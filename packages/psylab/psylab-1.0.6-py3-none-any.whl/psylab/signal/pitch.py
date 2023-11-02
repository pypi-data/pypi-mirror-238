# -*- coding: utf-8 -*-

# Copyright (c) 2010-2021 Christopher Brown
#
# This file is part of Psylab.
#
# Psylab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Psylab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to https://github.com/cbrown1/psylab/
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

import collections
import collections.abc
import numpy as np
import scipy.signal

from .samp import ms2samp

def periodic(f, fs, dur, sig=[1.]):
    """Generates arbitrary periodic signals, the default is a click train

        Parameters
        ----------
        f: scalar
            Frequency in Hz.
        fs: scalar
            The sampling frequency.
        dur : scalar
            The duration in ms. 
        sig : array
            The signal to repeat. Defaults to a 1-sample click.

        Returns
        -------
        y : array
            The specified signal.
    """

    sig = np.array(sig)
    period = np.int32(float(fs)/f)
    stim_len = ms2samp(dur, fs)
    sig_len = len(sig)
    nperiods = np.int32(stim_len // period) + 1

    arr = np.zeros((period, nperiods))
    arr[0:sig_len, :] = sig

    this_train = arr.flatten(order='F')[0:stim_len]


def tone(f, fs, dur, **kwargs):
    '''Generates pure tones

        Parameters
        ----------
        f: scalar/array
            Frequency info. If f is a scalar, then a pure tone of fixed
            frequency is created. If f is a 2-element array, the values will be
            the start and end frequecies of a linear frequency sweep. If f is
            an array of length > 2, the values will be the instantaneous
            sinusoidal frequency of the resulting signal. In this case, dur will 
            be ignored, and the output signal will be the same length (the same 
            number of samples) as input f.
        fs: scalar
            The sampling frequency.
        dur : scalar
            The duration in ms. 

        Kwargs
        ------
        amp : scalar/array
            The amplitude of the signal. If amp is a scalar, the entire signal 
            is scaled to amp. If it is an array, it must be the same length as 
            the resulting signal, and the elements of amp will be the 
            instantaneous amplitude of the resulting signal. Amplitude values 
            less than or equal to 0 are assumed to be in units of dB (re:+-1), 
            and values greater than 0 are used to scale the waveform peak 
            linearly. [default is 1]
        phase : scalar/array
            The phase of the signal, in degrees. If phase is a scalar, it is the 
            starting phase of the signal. If it is an array, it must be the same 
            length as the resulting signal, and the elements of phase will be 
            the instantaneous phase of the signal. [default = 0]

        Returns
        -------
        y : array
            The specified signal.

        Notes
        -----
        Examples:

        # Generate a 1000-Hz pure tone, with a sample rate of 22050, a
        # duration of 1s, an amplitude of +-.9, and a cosine starting phase
        t = tone(1000, 44100, 1000, amp=.9, phase=180);

        # Generate a tone with an amplitude that is 3 dB down from peak (+-1.0)
        t = tone(1000, 44100, 1000, amp=-3);

        # Generate a linear tone sweep starting at 200 Hz and ending at 750 Hz
        t = tone((200, 750), 44100, 1000, amp=-3);

        # Generate 2-Hz FM (with 50 Hz mod depth), on a 500-Hz carrier
        fm = tone(tone(2, 44100, 1000) * 25 + 500, 44100);

    '''

    amp = kwargs.get('amp', 1.)
    phase = kwargs.get('phase', 0.)

    f = np.array(np.float64(f))
    fs = np.float64(fs)
    dur = np.int32(np.round((np.float64(dur) / 1000.) * fs))
    amp = np.array(np.float64(amp))
    phase = np.float64(phase)*np.pi/180.

    if f.size == 2:
        freq = np.linspace(f[0], f[1], dur)
    elif f.size == 1:
        freq = np.ones(dur) * f
    else:
        dur = np.int32(f.size)
        freq = f

    if amp.size == 2:
        if not amp[0] > 0 or not amp[1] > 0:
            raise Exception('When generating amplitude sweeps, linear scaling must be used (ie., .01 < amp < 1.0')
        amp1 = np.linspace(amp[0], amp[1], dur)
    elif amp.size == 1:
        if amp <= 0:
            amp1 = np.ones(dur) * 10. ** (amp / 20.)
        else:
            amp1 = np.ones(dur) * amp
    else:
        amp1 = amp

    return amp1 * np.sin(phase + (2. * np.pi * np.cumsum(freq) / fs))


def tcomplex(f, fs, dur, **kwargs):
    #, amp=1, ncomponents=100, offset=0, phase=0):
    '''Generates tone complexes
        
        Parameters
        ----------
        f :  scalar or array-like
            If scalar, the fundamental frequency of a harmonic complex, and 
            use ncomponents and offset to specify components. Or pass an 
            array to specify component frequencies of a generic tone complex
            (in this case ncomponents and offset arguments are ignored).
        fs : scalar
            sampling frequency
        dur : scalar
            duration in ms

        Kwargs
        ------
        amp : scalar or array-like
            amplitude values less than or equal to 0 are treated as dB (re: 
            +-1), and values greater than 0 will scale the waveform 
            peak linearly. (array of length ncomponents allows setting amp 
            of each component separately) default = 1
        ncomponents : scalar
            number of harmonic components. Ignored if f is an array. 
            default = 100
        offset : scalar or array-like
            offset in Hz. Eg., offset = 2 would yield 102, 202, 302, 402, etc.
              (array of length ncomponents allows setting offset of each 
              component separately) Ignored if f is an array. default = 0
        phase : scalar or array-like
            starting phase of each component. (array of length ncomponents 
            allows setting phase of each component separately) default = 0 

        Returns
        -------
        y : array
            The waveform
    '''

    amp = np.float64(kwargs.get('amp', 1.))
    phase = np.float64(kwargs.get('phase', 0.))
    ncomponents = np.float64(kwargs.get('ncomponents', 100.))
    offset = np.float64(kwargs.get('offset', 0.))

    if isinstance(amp, (collections.abc.Sequence, np.ndarray)):
        test = amp[0]
    else:
        test = amp
    if test <= 0:
        amp = 10. ** (amp / 10.)
    dur_s = np.int32(np.round((dur / 1000.) * fs))
    phase_r = phase*np.pi/180.

    if isinstance(f, (collections.abc.Sequence, np.ndarray)):
        fh = f
    else:
        fh = ((np.arange(ncomponents) + 1) * f) + offset
    out = np.sin(phase_r + 2*np.pi * np.cumsum(np.ones((dur_s,fh.size))*fh,axis=0) / fs) * amp
    return out.sum(axis=1)


def huggins(f=[], fs=44100, dur=2000):
    """create Huggins pitch stimuli

        Huggins pitch, also known as binaural pitch, is a 
        noise stimulus with a weak but audible pitch 
        component that can only be heard binaurally, and 
        which is created with an interaural phase shift at 
        the specified frequency or frequencies using a 2nd 
        order all pole filter.

        Note that good quality wired headphones are likely required 
        in order to perceive the pitch. 

        Parameters
        ----------
        f: scalar/array
            The frequency or frequencies which will have an interaural phase
            shift. For more than 1 frequency, f can be a list or other array-like
            type. If f is empty, this function will return 2 channels of 
            correlated (diotic) noise.
        fs: scalar
            The sampling frequency.
        dur : scalar
            The duration in ms. 

        Returns
        -------
        y : array
            A 2d array representing the stereo Huggins pitch stimulus.

    """
    freq = np.atleast_1d(freq)

    sig = np.random.randn(int(dur / 1000 * fs))
    sig = np.vstack((sig, sig)).T
    sig /= np.max(sig)

    c = .03
    r = 1 - ((c * np.pi * f) / fs) # Poles radius
 
    b1 = r**2
    b2 = -2 * r * np.cos(2 * np.pi * f / fs)
    b3 = np.ones(len(f))
    b = np.vstack((b1, b2, b3))
    a = np.flipud(b)
    for i in range(len(f)):
        sig[:, 1] = scipy.signal.lfilter(b[:,i], a[:,i], sig[:, 1])

    return sig

