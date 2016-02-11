The genetic algorithm and the scripts in the pythonscript directory require a
working Java 1.7 as well as a Python 2.7 installation including the networkx
and numpy packages.

**Create navigational hierarchies:**  
The scripts needed for the genetic algorithm need to be placed in a
subdirectory called pythonscripts. Currently these are:  
- filehandler.py  
- get-apsp.py  
- get-spanning-trees.py  
- stretch.py  
- ufitness.py  

To create navigational hierarchies run:  
*java -jar ga.jar networkfile*  
Use -h option to get help on the available options for the algorithm.

**Network format:**  
Networks need to be represented as edge lists with continuous node ids
starting at 1. The tool converter.jar can be used to transform arbitrary edge
lists to this format. However, be sure to delete comments in the edge list 
file first.  
*java -jar converter.jar edgelistfile targetfilename*

Since the genetic algorithm is working on spanning trees make sure to use
connected networks. The largest connected component of a network can be
extracted with the "get_largest_component.py" script. However, don't forget to
convert the target file with the converter, afterwards.  
*python get_largest_component.py --network networkfile --filename targetfilename*
	
The tool createDots.jar can be used to create .dot files (used by Graphviz) from the tree files
created by the genetic algorithm:  
*java -jar createDots.jar treedirectory*

A correctly formatted sample network file (the one used in the parametrization experiments) is included:  
*wiki-sample.txt*

Additionally, various utility scripts are included in the pythonscript folder.