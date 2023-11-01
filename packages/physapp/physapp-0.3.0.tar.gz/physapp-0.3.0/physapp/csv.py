# David THERINCOURT - 2023
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
Module d'importation et d'exportation de tableaux de données au format CSV.
Logiciels pris en compte : Latis, Regressi, RegAvi, AviMeca3

Example
-------

@author: David Thérincourt - 2023
"""

import numpy as np
from io import StringIO

def _normalise_file_name(fileName, encodage = 'utf-8') :
    """
    Normalise les séparateurs décimaux dans un fichier CSV en remplaçant les virgules par des points.

    Parameters
    ----------
    filename : str
        Nom du fichier.

    encodage : str, optionnel ('utf-8' par défaut)
        Encodage du fichier.

    Return
    ------
    file : StringIO object
        Contenu du fichier.
    """

    f = open(fileName,'r', encoding = encodage)
    data = f.read()
    f.close()

    return StringIO(data.replace(",","."))



def load_txt(fileName, sep = ';', skip_header = 1) :
    """
    Importe des données au format CSV à partir d'un fichier txt.
    
    Parameters
    ----------
    fileName : str
        Nom du fichier CSV.

    sep : str, optionnel (';' par défaut)
        Caractère de séparation des colonnes de données.

    skip_header : int, optionnel (1 par défaut)
        Nombre de ligne à sauter au début du fichier.
    
    Return
    ------
    (numpy.ndarray, numpy.ndarray, ...) : tuple of nump.ndarray
    """

    return np.genfromtxt(fileName, delimiter = sep, unpack = True, skip_header = skip_header)



def load_avimeca3_txt(fileName, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel AviMéca 3.
    
    Parameters
    ----------
    fileName : str
        Nom du fichier CSV.

    sep : str, optionnel (tabulation '\t'  par défaut)
        Caractère de séparation des colonnes de données.
    
    Return
    ------
    (numpy.ndarray, numpy.ndarray, ...) : tuple
        Tuple de tableaux numpy.
    """

    data = _normalise_file_name(fileName, encodage = 'cp1252') # iso-8859-1 ou CP1252

    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 3, comments = '#')




def load_regavi_txt(fileName, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel RegAvi.
    
    Parameters
    ----------
    fileName : str
        Nom du fichier CSV.

    sep :str, optionnel (tabulation '\t' par défaut)
        Caractère de séparation des colonnes de données 
    
    Return
    ------
    (numpy.ndarray, numpy.ndarray, ...) : tuple
        Tuple de tableaux numpy.
    """
    data = _normalise_file_name(fileName, encodage = 'ascii')

    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 2, comments = '#')



def load_regressi_txt(fileName) :
    """
    Importe des données au format TXT à partir du logiciel Regressi.
    
    Parameters
    ----------
    fileName : str
        Nom du fichier CSV.
    
    Return
    ------
    (numpy.ndarray, numpy.ndarray, ...) : tuple
        Tuple de tableaux numpy.
    """

    return np.genfromtxt(fileName, delimiter = "\t", unpack = True, skip_header = 2, comments = '')



def load_regressi_csv(fileName) :
    """
    Importe des données au format CSV à partir du logiciel Regressi.
    
    Parameters
    ----------
    fileName : str
        Nom du fichier CSV.
    
    Return
    ------
    (numpy.ndarray, numpy.ndarray, ...) : tuple
        Tuple de tableaux numpy.
    """
    data = _normalise_file_name(fileName, encodage = 'ascii')

    return np.genfromtxt(data, delimiter = ";", unpack = True, skip_header = 2, comments = '')


def load_oscillo_csv(fileName):
    """
    Importe des données au format CSV à partir d'un oscilloscope numérique
    Tester avec oscilloscope Keysight InfiniiVision 2000 X-Series et 3000 X-Series
    
    Parameters
    ----------
    fileName : str
        Nom du fichier CSV
        
    Return
    ------
    (numpy.ndarray, numpy.ndarray, ...) : tuple
        Tuple de tableaux numpy.
    """

    return np.genfromtxt(fileName, delimiter = ",", unpack = True, skip_header = 2, comments = '#')



def load_ltspice_csv(fileName):
    """
    Importe des données au format CSV à partir du logiciel LTSpice.
    
    Parameters
    ----------
    fileName : str
        Nom du fichier CSV
        
    Returns
    -------
    (numpy.ndarray, numpy.ndarray, ...) : tuple
        Tuple de tableaux numpy.
    """
    
    return np.genfromtxt(fileName, delimiter = "\t", unpack = True, skip_header = 1, comments = '#')


#######################################
# Exportation
#######################################

def save_txt(data, fileName, sep = ";", headerLine = ''):
    """
    Exporte des données au format CSV dans un fichier texte (TXT) compatible Regressi, Latis, Libre office.
    Ecrase le fileName existant.
    
    Parameters
    ----------
    data : tuple of numpy.ndarray
        Tuple des tableaux numpy à exporter.

    fileName : str, optionnel ("data.txt" par défaut)
        Nom du fichier CSV à exporter.

    sep : str, optionnel (";" par défaut)
        Caractère de séparation des colonnes de données.

    headerLine : str, optionnel ('' par défaut)
        Noms des variables contenant les données séparés par le caractère de séparation défini par sep.

    Return
    ------
    None
    """

    data = np.transpose(data)
    np.savetxt(fileName, data, delimiter = sep, header = headerLine, comments='')

    return None
