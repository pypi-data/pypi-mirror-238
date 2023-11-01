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
Fonctions mathématique

@author: David Thérincourt
"""

import numpy as np

#--------------------------
# Fonctions mathématiques
#--------------------------


def lineaire(x, params) :
    a = params
    return a*x

def affine(x, *args):
    a, b = args
    return a*x + b

def parabole(x, *args) :
    a, b, c = args
    return a*x**2+b*x+c


def exponentielle_croissante(x, *args):
    """
    Fonction exponentielle croissante du type y = A*(1-exp(-x/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, tau = args
    return A*(1-np.exp(-x/tau))

def exponentielle_croissante_x0(x, *args):
    """
    Fonction exponentielle croissante du type y = A*(1-exp(-(x-x0)/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.:
    x0 (float) : retard.
    
    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, tau, x0 = args
    return A*(1-np.exp(-(x-x0)/tau))


def exponentielle_decroissante(x, *args):
    """
    Fonction exponentielle décroissante du type y = A*exp(-x/tau)

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, tau = args
    return A*np.exp(-x/tau)

def exponentielle_decroissante_x0(x, *args):
    """
    Fonction exponentielle décroissante du type y = A*exp(-(x-x0)/tau)

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    x0 (float) : retard.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, tau, x0 = args
    return A*np.exp(-(x-x0)/tau)

def exponentielle2_croissante(x, *args):
    """
    Fonction exponentielle croissante du type y = A*(1-exp(-k*x))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    k (float) : coefficient.
    
    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, k = args
    return A*(1-np.exp(-k*x))

def exponentielle2_croissante_retard(x, *args):
    """
    Fonction exponentielle croissante du type y = A*(1-exp(-k*(x-x0)))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    k (float) : coefficient.
    x0 (float) : retard.
    
    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, k, x0 = args
    return A*(1-np.exp(-k*(x-x0)))


def exponentielle2_decroissante(x, *args):
    """
    Fonction exponentielle décroissante du type y = A*exp(-k*x))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    k (float) : coefficient.
    
    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, k = args
    return A*np.exp(-k*x)

def exponentielle2_decroissante_retard(x, *args):
    """
    Fonction exponentielle décroissante du type y = A*exp(-k*(x-x0)))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    k (float) : coefficient.
    x0 (float) : retard.
    
    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    A, k, x0 = args
    return A*np.exp(-k*(x-x0))


def puissance(x, *args):
    A, n = args
    return A*x**n


############## Ordre 1 - Passe-bas  ################
def ordre1_passe_bas_transmittance(f, *args):
    """
    Fonction transmittance d'un système d'ordre 1 passe-bas

    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        T0 (float)                 : amplification statique.
        f0 (float)                 : fréquence propre.

    Retourne :
        T (float)
    """
    T0, f0 = args
    return T0/np.sqrt(1+(f/f0)**2)


def ordre1_passe_bas_gain(f, *args):
    """
    Fonction gain d'un système d'ordre 1 passe-bas

        G = G0 - 20log(sqrt(1+(f/f0)^2))

    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.

    Retourne :
        G (float)
    """
    G0, f0 = args
    return G0 - 20*np.log10(np.sqrt(1+(f/f0)**2))

def ordre1_passe_bas_dephasage(f, *args):
    """
    Fonction déphasage d'un système d'ordre 1 passe-bas

        phi = - arctan(f/f0)

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.

    Retourne :
        phi en degré (float)
    """
    f0 = args[0]
    return -np.arctan(f/f0)*180/np.pi


############## Ordre 1 - Passe-haut  ################
def ordre1_passe_haut_transmittance(f, *args):
    """
    Fonction transmittance d'un système d'ordre 1 passe-haut.

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T0 (float)  : Amplification statique.
    f0 (float) : fréquence propre.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    T0, f0 = args
    return T0*(f/f0)/np.sqrt(1+(f/f0)**2)


def ordre1_passe_haut_gain(f, *args):
    """
    Fonction gain d'un système d'ordre 1 passe-haut.

        G = G0 + 20log(f/f0) - 20log(sqrt(1+(f/f0)^2))

    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.

    Retourne :
        G (float)
    """
    G0, f0 = args
    return G0 + 20*np.log10(f/f0) - 20*np.log10(np.sqrt(1+(f/f0)**2))


def ordre1_passe_haut_dephasage(f, *args):
    """
    Fonction déphasage d'un système d'ordre 1 passe-haut.

        phi = 90 - arctan(f/f0)

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.

    Retourne :
        phi en degré (float)
    """
    f0 = args[0]
    return 90 - np.arctan(f/f0)*180/np.pi




############## Ordre 2 - Passe-bas  ################
def ordre2_passe_bas_transmittance(f, *args):
    """
    Fonction transmittance d'un système d'ordre 2 passe bas.

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        T0 (float)                  : amplification statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        T (float)
    """
    T0, f0, m = args
    return T0/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)

def ordre2_passe_bas_gain(f, *args):
    """
    Fonction gain d'un système d'ordre 2 passe bas.

    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.
        m (float)                  : coefficient d'amortissement

    Retourne :
        G (float)
    """
    G0, f0, m = args
    return G0 - 20*np.log10(np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2))


def ordre2_passe_bas_dephasage(f, *args):
    """
    Fonction déphasage d'un système d'ordre 2 passe bas.

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.
        m (float)                   : coefficient d'amortissement

    Retourne :
        phi en degré (float)
    """
    f0, m = args

    f1 = f[np.where(f<=f0)]
    phi1 = - np.arctan((2*m*f1/f0)/(1-(f1/f0)**2))*180/np.pi
    f2 = f[np.where(f>f0)]
    phi2 = -180 - np.arctan((2*m*f2/f0)/(1-(f2/f0)**2))*180/np.pi  # -180 car Im < 0
    return np.concatenate((phi1, phi2))


############## Ordre 2 - Passe-haut  ################
def ordre2_passe_haut_transmittance(f, *args):
    """
    Fonction transmittance d'un système d'ordre 2 passe-haut.

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        T0 (float)                  : amplification statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        T (float)
    """
    T0, f0, m = args
    return T0*(f/f0)**2/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)


def ordre2_passe_haut_gain(f, *args):
    """
    Fonction gain d'un système d'ordre 2 passe-haut.


    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        G0 (float)                  : gain statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        G (float)
    """
    G0, f0, m = args
    return G0 + 20*np.log10((f/f0)**2) - 20*np.log10(np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2))


def ordre2_passe_haut_dephasage(f, *args):
    """
    Fonction déphasage d'un système d'ordre 2 passe-haut.


    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        phi en degré (float)
    """
    f0, m = args

    f1 = f[np.where(f<=f0)]
    phi1 = 180 - np.arctan((2*m*f1/f0)/(1-(f1/f0)**2))*180/np.pi
    f2 = f[np.where(f>f0)]
    phi2 = -np.arctan((2*m*f2/f0)/(1-(f2/f0)**2))*180/np.pi      # -180 car Im < 0
    return np.concatenate((phi1, phi2))


############## Ordre 2 - Passe-bande  ################
def ordre2_passe_bande_transmittance(f, *args):
    """
    Fonction transmittance d'un système d'ordre 2 passe-bande.

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        T0 (float)                  : Amplification statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        T (float)
    """
    T0, f0, m = args
    return T0*2*m*(f/f0)/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)


def ordre2_passe_bande_gain(f, *args):
    """
    Fonction gain d'un système d'ordre 2 passe-bande.


    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.
        m  (float)                 : coefficient d'amortissement

    Retourne :
        G (float)
    """
    G0, f0, m = args
    return G0 + 20*np.log10(2*m*f/f0) - 20*np.log10(np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2))


def ordre2_passe_bande_dephasage(f, *args):
    """
    Fonction déphasage d'un système d'ordre 2 passe-bande.


    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        phi en degré (float)
    """
    f0, m = args

    f1 = f[np.where(f<=f0)]
    phi1 = 90 - np.arctan((2*m*f1/f0)/(1-(f1/f0)**2))*180/np.pi
    f2 = f[np.where(f>f0)]
    phi2 = -90 - np.arctan((2*m*f2/f0)/(1-(f2/f0)**2))*180/np.pi   # -180 car Im < 0
    return np.concatenate((phi1, phi2))
    
    