L'objectif de ce projet est l'apprentissage et la manipulation de la bibliothèque manim
Les animations sont plutôt simple à prendre en main, dans un premier temps.
La généricité du code prend du temps et pose de vrais questions d'organisation de code mais est très formateur pour débuter dans l'architecturage de projet.


## Projet 1
Le premier projet consiste en la réalisation d'une présentation vidéo dans le cadre de la présentation d'un autre projet portant sur la séparation d'une image en cartoon + textures. La présentation était initialement prévue
sous forme de powerpoint mais la découverte de la bibliothèque m'a conduit à mettre beaucoup de temps dans ce code.

La génération de la vidéo se fait via le terminal dans le répertoire du fichier principal (modelTV.py) en exécutant la commande:
manim -ql modelTV.py ModelTV (qualité low)
manim -qh modelTV.py ModelTV (qualité élevée)
