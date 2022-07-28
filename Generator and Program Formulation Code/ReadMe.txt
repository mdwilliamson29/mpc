Running "python run..." for the appropriate file will generate results in their corresponding folders in this directory. See the current folders for example outputs. These output files can be parsed for runtimes and averaged to obtain the results reported in the paper.

For example, running "python runILP.py" will the pathILP.py file 25 times for n = 10, 20, ..., 100. Each time pathILP.py is run with three parameters:
n, graphType, probability, where probability plays a role if the graphType is 0 indicating an Erdos-Renyi graph. In that case, probability denotes the probability of 
inserting an edge between two given nodes in the graph.