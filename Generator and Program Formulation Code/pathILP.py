from __future__ import print_function
from amplpy import AMPL

#import cplex
import random
import sys
import math
import time
import copy
import numpy as np
import os
#from networkx.generators.random_graphs import erdos_renyi_graph
import networkx.generators
import networkx
from graphviz import Digraph

# LTLstr = !danger U tool
S = [0, 1, 2, 3, 4, 5, 6, 7, 8]
betas = {0: 1}
n = int(sys.argv[1])
graphType = int(sys.argv[2])
probability = float(sys.argv[3])
#useCuts = int(sys.argv[3])

if graphType == -1:
    stronglyConnected = False
    while not stronglyConnected:
        g = networkx.generators.random_graphs.erdos_renyi_graph(n, probability, directed=True)
        stronglyConnected = networkx.is_strongly_connected(g)
if graphType == 0:
	g = networkx.generators.wheel_graph(n)
elif graphType == 1:
	g = networkx.generators.turan_graph(n, 5)
elif graphType == 2:
	g = networkx.generators.ladder_graph(int(n / 2))
elif graphType == 3:
	g = networkx.generators.circular_ladder_graph(int(n / 2))
elif graphType == 4:	
	# Complete bipartite graph
	g = networkx.generators.complete_multipartite_graph(int(n / 2), int(n / 2))
elif graphType == 5:
	g = networkx.generators.complete_graph(n)
else:
	g = networkx.generators.barbell_graph(int(n / 2), 0)

g = networkx.DiGraph(g)

#print(g.nodes)
# [0, 1, 2, 3, 4, 5]
#print(g.edges)
# [(0, 1), (0, 2), (0, 4), (1, 2), (1, 5), (3, 4), (4, 5)]

#for (a, b) in g.edges:
#	g.add_edge(1, 0)

#print(g.edges)

s = 0
t = n - 1

#print("s: " + str(s))
#print("t: " + str(t))

solutionType = 0 #int(sys.argv[2])

#constant = 1e9
#epsilon = 1e-6 #float(sys.argv[3]) #1e-5
#optTolerance = 1e-9 #float(sys.argv[4]) #1e-6
#feasTolerance = 1e-9 #float(sys.argv[5]) #1e-6
#intTolerance = 1e-8 #float(sys.argv[6]) #1e-5; apparently should be greater than feasTolerance

xIndices = []
xEdges = []
xCost = []
indexNum = 0
for (a, b) in g.edges:
	xIndices.append('x({0}, {1})'.format(a, b))
	xEdges.append((a, b))
	xCost.append(random.randint(0, n))
	indexNum += 1
	
	
wIndices = []
wEdges = []
cost = []
indexNum = 0
#n = 4
#g.clear()
#g.add_node(0)
#g.add_node(1)
#g.add_node(2)
#g.add_node(3)
#g.add_edge(0, 1)
#g.add_edge(0, 2)
#g.add_edge(1, 2)
#g.add_edge(1, 3)
#g.add_edge(2, 3)
#g.update([[(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)], [0, 1, 2, 3]])
#g.edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
#t = 3
#xEdges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
for (a, b) in g.edges: 
	for (c, d) in g.edges:
		if b == c:
			wIndices.append('w(({0}, {1}), ({2}, {3}))'.format(a, b, c, d))
			#wIndices.append(indexNum)
			wEdges.append(((a, b), (c, d)))
			cost.append(random.randint(0, n))
			indexNum += 1

for (c, d) in [(a2, b2) for (a2, b2) in xEdges if a2 == s]:
    wIndices.append('w((0, 0), ({0}, {1}))'.format(c, d))
    #wIndices.append(indexNum)
    wEdges.append(((0, 0), (c, d)))
    cost.append(xCost[xEdges.index((c, d))]) # Is this correct?
    indexNum += 1

#print("xIndices")
#print(xIndices)
#print("wIndices")
#print(wIndices)

buildTime = time.time()

ampl = AMPL()

ampl.eval('param cost{1..' + str(len(wEdges)) + '};')
costParam = ampl.getParameter('cost')
costParam.setValues(cost)
#print(costParam.getValues())
#for i in range(len(wEdges)):
#    ampl.getParameter(i + 1).setParameter(cost[i])
ampl.eval('var v{1..' + str(n) + '} integer >= 0, <= ' + str(n) + ';')
ampl.eval('var x{1..' + str(len(g.edges)) + '} binary;')
ampl.eval('var w{1..' + str(len(wEdges)) + '} binary;')
ampl.eval('minimize totalCost: sum {p in 1..' + str(len(wEdges)) + '} cost[p] * w[p];')
ind = 0

""" Constraint (i) """
for (a, b) in g.edges:
    #ampl.eval('subject to const' + str(ind) + ': 0 <= v[1] <= 1;')
    temp = 'subject to const' + str(ind) + ': v[' + str(b + 1) + '] >= v[' + str(a + 1) + '] + ' + str(n + 1) + ' * x[' + str(xEdges.index((a, b)) + 1) + '] - ' + str(n) + ';'
    #print(temp)
    ampl.eval(temp)
    ind += 1

""" Constraint (ii) """
for ((a, b), (c, d)) in wEdges:
    if (a, b) != (0, 0):
        temp = 'subject to const' + str(ind) + ': x[' + str(xEdges.index((a, b)) + 1) + '] + x[' + str(xEdges.index((c, d)) + 1) + '] - 1 <= w[' + str(wEdges.index(((a, b), (c, d))) + 1) + '];'
        #print(temp)
        ampl.eval(temp)
        ind += 1

""" Constraint (iii) """
for (c, d) in [(a2, b2) for (a2, b2) in xEdges if a2 == s]:
    temp = 'subject to const' + str(ind) + ': w[' + str(wEdges.index(((0, 0), (c, d))) + 1) + '] = x[' + str(xEdges.index((c, d)) + 1) + '];'
    #print(temp)
    ampl.eval(temp)
    ind += 1

adj = [[] for (c, d) in xEdges]
for ((a, b), (c, d)) in wEdges:
	adj[xEdges.index((c, d))].append((a, b)) 

""" Constraint (iv) """
for (c, d) in xEdges: #[(a2, b2) for (a2, b2) in xEdges if a2 != s]:
    #temp2 = ''
    #for ((a, b), (c2, d2)) in [((a3, b3), (c3, d3)) for ((a3, b3), (c3, d3)) in wEdges if (c3, d3) == (c, d)]:
    #    temp2 += 'w[' + str(wEdges.index(((a, b), (c2, d2))) + 1) + '] + '
    #print(temp2)
    temp2 = ''
    for (a, b) in adj[xEdges.index((c, d))]:
        temp2 += 'w[' + str(wEdges.index(((a, b), (c, d))) + 1) + '] + '
    #print(temp2)
    if len(temp2) > 0:
        temp = 'subject to const' + str(ind) + ': ' + temp2[:-3] + ' <= x[' + str(xEdges.index((c, d)) + 1) + '];'
        #print(temp)
        ampl.eval(temp)
        ind += 1

del adj

""" Constraint (v) """
for i in range(n):
    if i != s and i != t:
        H = [(a, b) for (a, b) in g.edges if b == i]
        T = [(a, b) for (a, b) in g.edges if a == i]
        #print(str(i + 1))
        #print(H)
        #print(T)
        tempLHS = ''
        tempRHS = ''
        for (a, b) in H:
            tempLHS += 'x[' + str(xEdges.index((a, b)) + 1) + '] + '
        for (a, b) in T:
            tempRHS += 'x[' + str(xEdges.index((a, b)) + 1) + '] + '
        if len(tempLHS) > 0 and len(tempRHS) > 0:
            temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' = ' + tempRHS[:-3] + ';'
            #print(temp)
            ampl.eval(temp)
            ind += 1
        elif len(tempLHS) > 0 and len(tempRHS) == 0:
            temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' = 0;'
            #print(temp)
            ampl.eval(temp)
            ind += 1
        elif len(tempLHS) == 0 and len(tempRHS) > 0:
            temp = 'subject to const' + str(ind) + ': ' + tempRHS[:-3] + ' = 0;'
            #print(temp)
            ampl.eval(temp)
            ind += 1
        """ Constraint (vi) """
        if len(tempLHS) > 0 and len(tempRHS) > 0:
            temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' <= 1;'
            #print(temp)
            ampl.eval(temp)
            ind += 1
        
""" Constraint (vii) """
tempLHS = ''
H = [(a, b) for (a, b) in g.edges if b == t]
#print(H)
for (a, b) in H:
    tempLHS += 'x[' + str(xEdges.index((a, b)) + 1) + '] + '
temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' = 1;'
#print(temp)
ampl.eval(temp)
ind += 1

""" Constraint (viii) """
tempLHS = ''
T = [(a, b) for (a, b) in g.edges if a == s]
#print(T)
for (a, b) in T:
    tempLHS += 'x[' + str(xEdges.index((a, b)) + 1) + '] + '
temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' = 1;'
#print(temp)
ampl.eval(temp)
ind += 1

""" Cut (i) """
"""if useCuts:"""

print("AMPL took " + str(time.time() - buildTime) + " seconds to build model!")

#ampl.eval('subject to (i) {e in 1..' + len(g.edges) + '}: sum {p in PATTERNS} rolls[w,p]* Cut[p]<= order[w]+ overrun;')
ampl.setOption('solver', 'cplex')
ampl.setOption('cplex_options', 'maxtime 3600')
#ampl.setOption('cplex_options', 'iisfind 1')
startTime = time.time()
ampl.solve()
print("ampl.solve() took " + str(time.time() - startTime) + " seconds!")
#ampl.eval('display _varname, _var.iis, _conname, _con.iis;')
totalCost = ampl.getObjective('totalCost')
print("Objective is:", totalCost.value())
