# Real Time Information System

Ce projet a été réalisé par **Lavigne Lucas** (IPSA) dans le cadre du cours sur les systèmes d'information en temps réel. Il a pour but d'analyser les performances et la distribution des temps d'exécution d'un programme afin d'en déduire des statistiques critiques pour les systèmes temps réel, telles que le pire temps d'exécution (**WCET** - Worst-Case Execution Time).

## Contenu du Projet

Le dépôt contient les fichiers suivants :

*   **`multiply.c`** : Un programme en langage C qui génère deux nombres aléatoires (jusqu'à 1 000 000) et les multiplie.
*   **`multiply.py`** : Le script principal en Python. Il s'occupe de la compilation du fichier C, de son exécution répétée (100 000 itérations), de la mesure du temps de chaque exécution, et de l'affichage des statistiques (Min, Max, Q1, Q2, Q3, WCET) ainsi que d'un histogramme des résultats.
*   **`rapport.tex`** : Un rapport rédigé en LaTeX présentant une analyse détaillée du système d'information en temps réel, de ses technologies et des défis associés.

## Prérequis

Pour pouvoir exécuter ce projet sur votre machine, vous devez disposer des outils suivants :

1.  **Python 3.x** installé sur votre machine.
2.  **GCC** (Compilateur C) installé et accessible depuis vos variables d'environnement (`PATH`), afin que le script Python puisse compiler le code C.
3.  *(Optionnel)* Une distribution LaTeX (comme TeX Live ou MiKTeX) pour compiler le fichier `rapport.tex`.

### Installation des dépendances Python

Le script Python utilise `numpy` pour le calcul des quartiles et `matplotlib` pour l'affichage du graphique. Installez-les via `pip` :

```bash
pip install numpy matplotlib
```

## Utilisation

Pour lancer l'analyse complète, exécutez simplement le script Python depuis votre terminal :

```bash
python multiply.py
```

**Déroulement du script :**
1. Le script compile automatiquement `multiply.c` en un exécutable `multiply.exe`.
2. Il lance l'exécutable 100 000 fois en mesurant précisément le temps de chaque exécution, tout en affichant un pourcentage de progression.
3. Il affiche les statistiques globales dans le terminal (Temps minimum, maximum, quartiles et WCET).
4. Il ouvre une fenêtre générant un histogramme pour visualiser la distribution des temps d'exécution.