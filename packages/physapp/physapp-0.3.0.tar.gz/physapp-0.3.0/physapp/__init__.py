# David THERINCOURT - 2022
#
# The MIT License (MIT)
#
# Copyright (c) 2014-2019 Damien P. George
# Copyright (c) 2017 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Librairie Python 3 pour la physique appliquée

Example
-------

from physapp.modelisation import ajustement_lineaire


@author: David Thérincourt - 2023
"""

from physapp.base import derive, integrale, spectre_amplitude, spectre_RMS, spectre_RMS_dBV
from physapp.csv import load_txt, load_avimeca3_txt, load_regavi_txt, load_regressi_txt, load_regressi_csv, load_oscillo_csv, load_ltspice_csv, save_txt
from physapp.modelisation import *

