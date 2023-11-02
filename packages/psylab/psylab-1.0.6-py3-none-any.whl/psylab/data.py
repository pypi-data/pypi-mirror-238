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
# contributions are welcome. Go to http://github.com/cbrown1/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import numpy as np

def read_csv(filename, comment="#"): 
    """Gracefully handle comments and blank lines when reading csv files.
    
        Pandas is great, but doesn't do a good job with headers. This function 
        skips blank and comment lines in a csv properly, and passes back a 
        file-like object ready to be passed to pandas.read_csv.
        
        Parameters
        ----------
        filename : string
            The path to the csv file.
        comment : string
            A comment character to look for. Lines that start with this 
            character will be skipped. 

        Returns
        -------
        StringIO object
            A file-like object, suitable to be passed to pandas.read_csv.
            
        Usage
        -----
        f = read_csv(filename)
        data = pandas.read_csv(f, **kwargs)
    """
    lines = ""
    for line in open(filename):
        line = line.strip()
        if not line.startswith(comment):
            if line != "":
                lines += line + "\n"
    return StringIO(lines)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def random_derangement(n):
    """Generates a random permutation of size n with no fixed points.
    
        Returns a numpy array of ints in which no value is equal to its index.
        
        Parameters
        ----------
        n : int
            The length of the array
            
        Returns
        -------
        a : array
            The array
        
        Notes
        -----
        This was adapted from an answer to a stackoverflow question, and 
        apparently implements the "early refusal" algorithm. 
    
    """
    while True:
        v = np.arange(n)
        for j in np.arange(n - 1, -1, -1):
            p = np.random.randint(0, j+1)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return v


def find_reversals(data, which="all"):
    """Find the reversals in a dataset

    Returns the indices of the reversals in an array of data 
    as would occur in an n-alternative adaptive tracking run

    Parameters
    ----------
    data : Array like
        The data to use
    which : str
        Which reversals to return. Possible values are 'ups', 'downs', or 
        'all' [default]. 'ups' returns all values that are greater than 
        the previous value when the previous value was less than or equal
        to the value before it. 'downs' returns all values that are the 
        opposite. 'all' returns both 'ups' and 'downs'.

    Returns
    -------
    inds : Array
        An array of the indices of the specified reversals in data

    Usage
    -----
    >>> data = np.array([8,8,7,7,6,6,5,5,4,5,5,4,4,3,4,5,5,4,4])
    >>> revs = find_reversals(data)
    >>> revs
    array([ 8, 10, 13, 16], dtype=int32)
    >>> data[revs]
    array([4, 5, 3, 5])
    >>> plot(data)
    >>> plot(revs, data[revs], 'o', ms = 9, mfc='None')
    """

    trial_n = 0
    rev_all_i = []
    rev_ups_i = []
    rev_dns_i = []
    rev_all_val = []
    rev_ups_val = []
    rev_dns_val = []
    val_prev = None
    direction_prev = 0
    direction_curr = 0
    for val in data:
        if val_prev != None:
            if val_prev > val:
                direction_curr = -1
            elif val_prev < val:
                direction_curr = 1

            if direction_prev > direction_curr:
                # Down
                if direction_prev != 0:
                    #np.append(rev_all_i, int(trial_n)-1)
                    #np.append(rev_dns_i, int(trial_n)-1)
                    rev_all_i.append(int(trial_n)-1)
                    rev_dns_i.append(int(trial_n)-1)
                    rev_all_val.append(val_prev)
                    rev_dns_val.append(val_prev)
                direction_prev = direction_curr
            elif direction_prev < direction_curr:
                # Up
                if direction_prev != 0:
                    #np.append(rev_all_i, int(trial_n)-1)
                    #np.append(rev_ups_i, int(trial_n)-1)
                    rev_all_i.append(int(trial_n)-1)
                    rev_ups_i.append(int(trial_n)-1)
                    rev_all_val.append(val_prev)
                    rev_ups_val.append(val_prev)
                direction_prev = direction_curr

        val_prev = val
        trial_n += 1

    if which == 'ups':
        return np.array(rev_ups_i, dtype=np.int32)
    elif which == 'downs':
        return np.array(rev_dns_i, dtype=np.int32)
    else:
        return np.array(rev_all_i, dtype=np.int32)
