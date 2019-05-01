# Partie Transpilation

Cette partie s'appuie sur [textX](https://github.com/textX/textX "textX' GitHub HomePage") et a pour but de permettre la transpilation d'un fichier contant des expressions OCL vers un fichier Python contenant les mêmes expressions traduites, éventuellement en manipulant des objets Python issus de la bibliothèque de Wrappers proposés dans la seconde partie du projet.

Le fichier __oclGrammar.tx__ contient la grammaire en [textX](https://github.com/textX/textX "textX' GitHub HomePage") pour les expressions qui nous intéressent.

Le fichier __expression.ocl__ présente des exemples des expressions OCL qui nous intéressent.

Il est possible d'utiliser les commandes suivantes afin de visualiser le résultat du "parsage" de ces expressions par [textX](https://github.com/textX/textX "textX' GitHub HomePage") utilisant cette grammaire (nécéssite [Graphviz](https://www.graphviz.org/ "Graphviz' Homepage")) :
```
$>: textx visualize ocl.tx expression.ocl
$>: dot -Tpng -O expression.ocl.dot
```

Le fichier __oclParserDev.py__ contient le code en cours de développement du Transpilateur et s'utilise de la manière suivante :
```
$>: python oclParserDev.py -i expression.ocl -g oclGrammar.tx -o result.txt
```

## Deboggage

Le détail du travail du transpilateur est stocké dans `log.txt`. Utilisez l'option `-v` pour activer le mode Verbose et que les mêmes messages soient aussi envoyés à la sortie standard.

Ajoutez l'option `-d` pour le mode Debug, pendant lequel textX va générer des fichiers détaillant son travail :
* File_parser_model.dot
  Fichier Dot qui présente la grammaire utilisée sous forme d'un graphe.
* Model_parse_tree.dot
  Fichier Dot qui présente le fichier input sous forme de graphe correspondant la grammaire utilisé.

Ces deux fichiers sont visualisables en générant un PNG pour chacun via la même commande que décrite plus haut :
```
$>: dot -Tpng -O File_parser_model.dot
```
et
```
$>: dot -Tpng -O Model_parse_tree.dot
```
