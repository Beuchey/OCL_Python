# OCL_Python

Ce projet a pour but de proposer des outils de transpilation de OCL vers Python.

Deux méthodes complémentaires sont explorées :
  * Une partie Transpilation (appliquer un transpilateur sur des expressions OCL afin de produire un fichier Python ayant les mêmes fonctionnalités car manipulant des Wrappers)
  * Une partie Wrapper (une bibliothèque permettant de simuler les fonctionnalités d'OCL en restant dans Python)

## Sujet

Les fonctionnalités OCL visées sont décrites dans le dossier __FonctionnalitésOCL/__ où on peut trouver le fichier __Correspondances.md__. Ce fichier liste les fonctionnalités étudiées (pour l'instant seuls les Objets concernés sont présents, les Expressions viendront sous peu) ainsi que leur détail et le code Python proposé comme correspondant.

Pour les Objets OCL et leur méthodes, le détail de la proposition de correspondance peut être trouvé dans __Wrapper/pistes/__.

Pour les Expressions OCL, le détail du méchanisme se situe dans __Transpilation__.

## Partie 1 : Transpilation

Cette partie s'appuie sur [textX](https://github.com/textX/textX "textX' GitHub HomePage") et a pour but de permettre la transpilation d'un fichier contant des expressions OCL vers un fichier Python contenant les mêmes expressions traduites, éventuellement en manipulant des objets Python issus de la bibliothèque de Wrappers proposés dans la seconde partie du projet.

## Partie 2 : Wrapper

Une bibliothèque d'objets et de fonctions permettant d'écrire du Python dont les fonctionnalités et la syntaxe de raprochent le plus possible d'OCL, afin de produire du code "OCL-like" interprétable par Python.

Le module __oclpyth/__ propose un fichier __OCLPyth.py__ qui reprend l'ensemble des propositions retenues en un exemple fonctionnel.
A la fin de celui-ci se trouvent plusieurs exemples illustrant chacun une des fonctionnalités explorées sont disponibles pour être décommentés et étudiés.
