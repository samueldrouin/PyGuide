# GUIDE-CFR

Le programme GUIDE-CFR est une version adaptée pour le Centre de femmes du Haut-Richelieu du programme C++ GUIDE. Le programme permet la gestion des activités, des membres et comporte un module de facturation.

## Pour commencer

Le programme est basé sur PyQt et Python 3.6 afin de permettre l'installation sur une grande variété de système d'exploitation. Cependant, seul le système Microsoft Windows est pleinement supporté. Pour cette raison, même si l'installation et l'opération du programme sur Linux et MacOS est possible, seule les instruction d'installation sur Windows seront fournies. 

### Prérequis

Le programme nécessite l'installation des programmes suivants pour fonctionner : 
* Python 3.6 et plus récent
* PyQt 5.9.2 et plus récent

Installer d'abord la distribution Python 3 pour Windows la plus récente (https://www.python.org).

Pour installer PyQt5, ouvrez le Terminal puis entrez le code :
```
pip3 install PyQt5
```

Pour utiliser certains modules de l'application tel que la génération de rapports, il est aussi nécessaire d'installer une distribution LaTeX. 

La distribution LaTeX recommandé pour les utilisateurs qui n'ont jamais utilisés LaTeX est MikTeX (https://miktex.org). L'installation de base est suffisante, cependant, elle n'inclue pas tout les paquets qui seront utilisés par le programme. Pour cette raison, il est recommandé de garder l'option d'installer des paquets manquants active.

### Installation

Le programme ne nécessite aucune étape d'installation. Il est possible de l'exécuter à partir de n'importe localisation sur le disque. 

Une fois le fichier téléchargé et installé dans la localisation où il doit être exécuté, lancer la commande terminal suivante pour l'exécuter. 
```
python3 /path/to/main.py
```
Si l'installation est correcte, le programme devrait s'ouvrir. 

## Déploiement

Il est nécessaire 

## Contribuer

Ce programme devrait servir uniquement à l'usage interne du Centre de femmes du Haut-Richelieu. Les individus ou corporations mendatés pour modifier le programme par le Centre de femmes du Haut-Richelieu peuvent créer de nouvelle branches pour modifier le programmes.

## Auteur

**Samuel Prince-Drouin** 2017-2018

## License

Le projet est sous license GPL 3 - référez vous au fichier [LICENSE.md](LICENSE.md) pour les détails. 
