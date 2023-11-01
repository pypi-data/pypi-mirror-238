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
Module pour le traitement des courbes et des signaux.

Fonctions
---------

    derive(y, x)
        
        | Retourne la dérivée de la fonction f(x) avec l'approximation :
        | dy/dx = (y[n+1]-y[n-1])/(x[n+1]-x[n-1])


    integrale(y, x, xmin, xmax)

        | Calcule une approximation l'intégrale de la fonction y=f(x) entre
        | les bornes xmin et xmax avec la méthode des trapèzes.
 
 
    spectre_amplitude(y, t, T)
        
        | Retourne le spectre d'amplitude d'un signal y(t).
 
 
    spectre_RMS(y, t, T, tmin=0, plot_period_ax=None)
        
        | Retourne le spectre RMS d'un signal y(t).
        
        
    spectre_RMS_dBV(y, t, T, tmin=0, plot_period_ax=None):
        
        | Retourne le spectre RMS en dBV d'un signal y(t).

Example
-------

from physapp import load_oscillo_csv, derive
t, u = load_oscillo_csv('scope.csv')
v = derive(u, t)
        
@author: David Thérincourt - 2023
"""

import numpy as np
from numpy.fft import fft
from scipy.integrate import trapz
from scipy.signal import correlate, find_peaks, peak_prominences




def derive(y, x):
    """ Retourne la dérivée de la fonction f(x) avec l'approximation :
    
                  dy/dx = (y[n+1]-y[n-1])/(x[n+1]-x[n-1])

    Parameters
    ----------
    y : numpy.ndarray
        Tableau Numpy des y.
    
    x : numpy.ndarray
        Tableau Numpy des x.

    Return
    ------
    d : numpy.ndarray
        Tableau Numpy de même dimension. La valeur Nan (Not A Number) est affectée
        pour la première valeur et la dernière valeur du tableau où la derivée n'est
        pas calculable !
    """
    
    N = len(y)
    d = [float('nan') for i in range(N)]
    for i in range(1, len(y)-1):
        d[i] = (y[i+1]-y[i-1])/(x[i+1]-x[i-1])
    return d





def integrale(y, x, xmin, xmax, plot_ax=None):
    """ Calcule une approximation l'intégrale de la fonction y=f(x) entre
    les bornes xmin et xmax avec la méthode des trapèzes.
    
    Parameters
    ----------
    y : numpy.ndarray
        Tableau Numpy des y.
        
    x : numpy.ndarray
        Tableau Numpy des x.

    xmin : float
        Borne inférieure pour l'intégration.

    xmax : float
        Borne supérieure pour l'intégration.

    plot_ax : matplotlib.axes, optionnel (None par défaut)
        Repère (axes) sur lequel tracé l'aire de l'intégration.
        
    Return
    ------
    aire : float
        Résultat de l'intégration.
    """

    if (xmin<x[0]) or (xmin>x[-2]):
        raise ValueError("Valeur de xmin en dehors de l'intervalle de x")
    if (xmax<x[1]) or (xmax>x[-1]):
        raise ValueError("Valeur de xmax en dehors de l'intervalle de x")
    if xmin>=xmax:
        raise ValueError("Valeur de xmin supérieure à la valeur de xmax")
    
    y = y[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    x = x[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    
    if plot_ax != None:
        plot_ax.fill_between(x,y,hatch='\\',facecolor='linen',  edgecolor='gray')
        
    return trapz(y)*(x[-1]-x[0])/len(x)




def spectre_amplitude(y, t, T, tmin=0, plot_period_ax=None):
    ''' Retourne le spectre d'amplitude d'un signal y(t).
    
    Parameters
    ----------
    y : numpy.ndarray
        Tableau des valeurs du signal.
        
    t : numpy.ndarray
        Tableau des temps.

    T : float
        Période du signal.

    tmin : float, optionnel (0 par défaut)
        Borne inférieure le calcul du spectre.

    plot_period_ax : matplotlib.axes, optionnel (None par défaut)
        Repère (axes) sur lequel tracer la sélection de la période.
        
    Return
    ------
    (f, A) : (numpy.ndarray, numpy.ndarray)
        Tableaux des fréquences et des amplitudes.
    '''
    
    if T>(t[-1]-t[0]):
        raise ValueError("Période T trop grande")
    
    if (tmin<t[0]) or (tmin>t[-2]):
        raise ValueError("Valeur de tmin en dehors de l'intervalle de t")
    
    tmax = tmin + T
    if tmax>t[-1]:
        raise ValueError("Valeur de tmin trop grande")
    
    if plot_period_ax != None:
        plot_period_ax.axvspan(tmin, tmax , color='linen')
    
    y = y[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    t = t[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    T = t[-1]-t[0]                   # Durée totale
    N = len(t)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    ampl = np.absolute(fft(y))/N     # 
    ampl[1:-1] = ampl[1:-1]*2        # Tableau des amplitudes
    
    return freq, ampl                # Retourne fréquences et amplitudes





def spectre_RMS(y, t, T, tmin=0, plot_period_ax=None):
    ''' Retourne le spectre RMS d'un signal y(t).
    
    Parameters
    ----------
    y : numpy.ndarray
        Tableau Numpy des y.
        
    t : numpy.ndarray
        Tableau Numpy des t.

    T : float
        Période du signal y.

    tmin : float, optionnel (0 par défaut)
        Borne inférieure le calcul du spectre.

    plot_period_ax : matplotlib.axes, optionnel (None par défaut)
        Repère (axes) sur lequel tracer la sélection de la période.
        
    Return
    ------
    (f, U) : (numpy.ndarray, numpy.ndarray)
        Tableaux des fréquences et des valeurs efficaces.
    '''
    
    if T>(t[-1]-t[0]):
        raise ValueError("Période T trop grande")
    
    if (tmin<t[0]) or (tmin>t[-2]):
        raise ValueError("Valeur de tmin en dehors de l'intervalle de t")
    
    tmax = tmin + T
    if tmax>t[-1]:
        raise ValueError("Valeur de tmin trop grande")
    
    if plot_period_ax != None:
        plot_period_ax.axvspan(tmin, tmax , color='linen')
    
    y = y[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    t = t[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    T = t[-1]-t[0]                   # Durée totale
    N = len(t)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    eff = np.absolute(fft(y))/N      # 
    eff[1:-1] = eff[1:-1]*np.sqrt(2) # Tableau des val. eff.
        
    return freq, eff                 # Retourne fréquences et valeurs RMS







def spectre_RMS_dBV(y, t, T, tmin=0, plot_period_ax=None):
    ''' Retourne le spectre RMS en dBV d'un signal y(t).
    
    Parameters
    ----------
    y : numpy.ndarray
        Tableau Numpy de y.
        
    t : numpy.ndarray
        Tableau Numpy de t.

    T : float
        Période du signal y.

    tmin : float, optionnel (0 par défaut)
        Borne inférieure le calcul du spectre.

    plot_period_ax : matplotlib.axes, optionnel (None par défaut)
        Repère (axes) sur lequel tracer la sélection de la période.
        
    Return
    ------
    (f, U_dBV) : (numpy.ndarray, numpy.ndarray)
        Tableaux des fréquences et des valeurs efficaces en dBV.
    '''
    
    if T>(t[-1]-t[0]):
        raise ValueError("Période T trop grande")
    if (tmin<t[0]) or (tmin>t[-2]):
        raise ValueError("Valeur de tmin en dehors de l'intervalle de t")
    
    tmax = tmin + T
    if tmax>t[-1]:
        raise ValueError("Valeur de tmin trop grande")
    
    if plot_period_ax != None:
        plot_period_ax.axvspan(tmin, tmax , color='linen')
    
    y = y[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    t = t[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    T = t[-1]-t[0]                   # Durée totale
    N = len(t)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    eff = np.absolute(fft(y))/N      # 
    eff[1:-1] = eff[1:-1]*np.sqrt(2) # Tableau des val. eff.
    
    return freq, 20*np.log10(eff)     # Retourne fréquences et valeurs RMS dBV
