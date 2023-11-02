# -*- coding: utf-8 -*-

# Copyright (c) 2010-2012 Christopher Brown
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

import numpy as np

def atten(data, dB):
    '''Attenuates input array by a dB value
    
        Positive dB values yield decreases in level, negative values 
        increase level.
        
        Parameters
        ----------
        data : ndarray
            Array containing numbers to attenuate. 
        dB : int
            The amount of attenuation, in dB. The default is to compute
            the mean of the flattened array.
        
        Returns
        -------
        data : array
            The input array, attenuated.
    '''
    return data * np.exp(np.float32(-dB)/8.6860)


def equate( *args ):
    """equate a
    """

    out = list()
    min_rms = np.finfo(np.float64).max

    for arg in args:
        this_rms = np.sqrt(np.mean(np.square(arg)))
        if min_rms > this_rms:
            min_rms = this_rms

    for arg in args:
        this_rms = np.sqrt(np.mean(np.square(arg)))
        arg *= min_rms / this_rms
        out.append(arg)

    return tuple(out)


def normalize( *args ):

    out = list()
    max_val = 0.

    for arg in args:
        this_max = np.max(arg)
        if max_val < this_max:
            max_val = this_max

    for arg in args:
        arg /= max_val
        out.append(arg)

    return tuple(out)
