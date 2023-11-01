# Librairie Python pour la physique appliquée

## Installation

Dans un terminal :

    pip install physapp

Mise à jour :

```python
pip install --upgrade physapp
```

---

## Dépendances

Cette librairie se base principalement sur les librairies `numpy`, `matplotlib` et `scipy`

---

## Module `physapp.base`

### > Fonctions disponibles

`derive(y, x)`

`integrale(y, x, xmin, xmax)`

`spectre_amplitude(y, t, T)`

`spectre_RMS(y, t, T)`

`spectre_RMS_dBV(y, t, T)`

### > Exemple

```python
import numpy as np
import matplotlib.pyplot as plt
from physapp import load_oscillo_csv, integrale

t, u = load_oscillo_csv('scope.csv')

f = 125
T = 1/f
aire = integrale(u, t, 0, T, plot_ax=plt)
moy = aire/T

plt.plot(t, u)
plt.axhline(moy, ls="--", color="C3")
plt.text(0.65*T, moy+0.2, "Moy = {:.2f} V".format(moy), color="C3")
plt.title("Valeur moyenne d'un signal périodique")
plt.xlabel("t (s)")
plt.ylabel("u (V)")
plt.grid()
plt.show()
```

![](https://david-therincourt.fr/python/pypi-physique/exemple_3.png)

## Module `physapp.modelisation`

Fonctions pour réaliser une modélisation d'une courbe du type `y=f(x)`.

### > Fonctions classiques

| Fonction                                       | Description          |
| ---------------------------------------------- | -------------------- |
| `ajustement_lineaire(x, y)`                    | $y=ax$               |
| `ajustement_affine(x, y)`                      | $y=ax+b$             |
| `ajustement_parabolique(x, y)`                 | $y=ax^2+bx+c$        |
| `ajustement_exponentielle_croissante(x, y)`    | $y=A(1-e^{-x/\tau})$ |
| `ajustement_exponentielle_decroissante(x, y)`  | $y = Ae^{-x/\tau}$   |
| `ajustement_exponentielle2_croissante(x, y)`   | $y = A(1-e^{-kx})$   |
| `ajustement_exponentielle2_decroissante(x, y)` | $y = Ae^{-kx}$       |
| `ajustement_puissance(x, y)`                   | $y=Ax^n$             |

### > Réponses fréquentielles

`ajustement_ordre1_passe_bas_transmittance(f, T)`

`ajustement_ordre1_passe_bas_gain(f, G)`

`ajustement_ordre1_passe_bas_dephasage(f, phi)`

`ajustement_ordre1_passe_haut_transmittanc(f, T)`

`ajustement_ordre1_passe_haut_gain(f, G)`

`ajustement_ordre1_passe_haut_dephasage(f, phi)`

`ajustement_ordre2_passe_bas_transmittance(f, T)`

`ajustement_ordre2_passe_haut_transmittance(f, T)`

`ajustement_ordre2_passe_bande_transmittance(f, T)`

`ajustement_ordre2_passe_bande_gain(f, G)`

### > Exemple

```python
import matplotlib.pyplot as plt
from physapp import ajustement_parabolique

x = [0.003,0.141,0.275,0.410,0.554,0.686,0.820,0.958,1.089,1.227,1.359,1.490,1.599,1.705,1.801]
y = [0.746,0.990,1.175,1.336,1.432,1.505,1.528,1.505,1.454,1.355,1.207,1.018,0.797,0.544,0.266]

modele = ajustement_parabolique(x, y)

plt.plot(x, y, '+', label="Mesures")
modele.plot()
plt.legend(facecolor="linen")
plt.title("Trajectoire d'un ballon")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid()
plt.show()
```

![](https://david-therincourt.fr/python/pypi-physique/exemple_1.png)

---

## Module `physapp.csv`

Module d'importation de tableau de données au format CSV à partir des logiciels Aviméca3, Regavi, ...

#### > Fonctions disponibles

`load_txt(fileName)`

`load_avimeca3_txt(fileName)`  

`load_regavi_txt(fileName)`

`load_regressi_txt(fileName)`

`load_regressi_csv(fileName)`

`load_oscillo_csv(filename)`

`load_ltspice_csv(filename)`

`save_txt(data, fileName)`

#### > Exemple

```python
import matplotlib.pyplot as plt
from physapp import load_avimeca3_txt

t, x, y = load_avimeca3_txt('data.txt')

plt.plot(x,y,'.')
plt.title("Trajectoire d'un ballon")
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.grid()
plt.show()
```

Le fichier `data.txt` a été exporté du logiciel Avimeca 3 à partir d'un exemple !

![](https://david-therincourt.fr/python/pypi-physique/exemple_2.png)
