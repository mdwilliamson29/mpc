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
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx
from graphviz import Digraph

# LTLstr = !danger U tool
S = [0, 1, 2, 3, 4, 5, 6, 7, 8]
betas = {0: 1}
n = int(sys.argv[1])
graphType = int(sys.argv[2])
probability = float(sys.argv[3])
useCuts = False #int(sys.argv[3])

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
xEdges.append((0, 0))
g.add_edge(0, 0)
xCost.append(0.0)
xObj = []
	
	
wIndices = []
wEdges = []
cost = [[0.0 for j in range(len(g.edges))] for i in range(len(g.edges))]
sc = [[0 for j in range(len(g.edges))] for i in range(len(g.edges))]
indexNum = 0

for (a, b) in g.edges: 
	for (c, d) in g.edges:
		if b == c:
			wIndices.append('w(({0}, {1}), ({2}, {3}))'.format(a, b, c, d))
			#wIndices.append(indexNum)
			wEdges.append(((a, b), (c, d)))
			xObj.append((xEdges.index((a, b)), xEdges.index((c, d))))
			#cost.append(random.randint(0, n))
			cost[xEdges.index((a, b))][xEdges.index((c, d))] = random.randint(0, n)
			sc[xEdges.index((a, b))][xEdges.index((c, d))] = 1
			indexNum += 1

for (a, b) in [(a2, b2) for (a2, b2) in xEdges if a2 == s]:
	xObj.append((xEdges.index((0, 0)), xEdges.index((a, b))))
	cost[xEdges.index((0, 0))][xEdges.index((a, b))] = xCost[xEdges.index((a, b))]
	sc[xEdges.index((0, 0))][xEdges.index((a, b))] = 1
	indexNum += 1

#print(xObj)

buildTime = time.time()

ampl = AMPL()
#xObj = [[1 for j in range(4)] for i in range(4)]
ampl.eval('param cost {1..' + str(len(g.edges)) + ', 1..' + str(len(g.edges)) + '};')
costParam = ampl.getParameter('cost')
costParam.setValues([y for x in cost for y in x])
#print(costParam.getValues())
#for i in range(len(wEdges)):
#    ampl.getParameter(i + 1).setParameter(cost[i])
ampl.eval('var v{1..' + str(n) + '} >= 0, <= ' + str(n) + ';')
ampl.eval('var x{1..' + str(len(g.edges)) + '} >= 0, <= 1;')
"""tempTail = ''
tempHead = ''
for ((a, b), (c, d)) in wEdges:
	tempTail += str(xEdges.index((a, b)) + 1) + ', '
	tempHead += str(xEdges.index((c, d)) + 1) + ', '
ampl.eval('set tail := {' + tempTail[:-3] + '};')
ampl.eval('set head := {' + tempHead[:-3] + '};')"""
ampl.eval('param sc {1..' + str(len(g.edges)) + ', 1..' + str(len(g.edges)) + '} >= 0;')
scParam = ampl.getParameter('sc')
"""sc = [[0 for j in range(len(g.edges))] for i in range(len(g.edges))]
for i in range(len(g.edges)):
	for j in range(len(g.edges)):
		if (i, j) in xObj:		
			sc[i][j] = 1"""
scParam.setValues([y for x in sc for y in x]) #[1 for j in range(len(g.edges) * len(g.edges))])
#ampl.eval('let {i in 1..' + str(len(g.edges)) + ', j in 1..' + str(len(g.edges)) + '} sc[i, j] := 1;')
scParam = ampl.getParameter('sc')
#print(scParam.getValues())
ampl.eval('set rt := {d in 1..' + str(len(g.edges)) + ', w in 1..' + str(len(g.edges)) + ': sc[d, w] = 1};')
#ampl.eval('var w{1..' + str(len(wEdges)) + '} binary;')
#ampl.eval('minimize totalCost: sum {p in 1..' + str(len(wEdges)) + '} cost[p] * w[p];')
ampl.eval('maximize totalCost: sum {(i, j) in rt} cost[i, j] * x[i] * x[j];')
#ampl.eval('minimize totalCost: (sum {(i, j) in 1..' + str(len(g.edges)) + '} sum{p2 in 1..' + str(len(g.edges)) + '} cost[p] * x[p] * x[p2]) + sum {p3 in 1..' + str(len(g.edges)) + '} ' + str(n * n) + 'x[p3] * (1 - x[p3]);')
ind = 0

""" Constraint (i) """
temp = 'subject to const' + str(ind) + ': x[' + str(xEdges.index((0, 0)) + 1) + '] = 1;'
#print(temp)
ampl.eval(temp)
ind += 1

""" Constraint (ii) """
for (a, b) in g.edges:
    if (a, b) != (0, 0):
    	#ampl.eval('subject to const' + str(ind) + ': 0 <= v[1] <= 1;')
    	temp = 'subject to const' + str(ind) + ': v[' + str(b + 1) + '] >= v[' + str(a + 1) + '] + ' + str(n + 1) + ' * x[' + str(xEdges.index((a, b)) + 1) + '] - ' + str(n) + ';'
    	#print(temp)
    	ampl.eval(temp)
    	ind += 1

""" Constraint (iii) """
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
        """ Constraint (iv) """
        if len(tempLHS) > 0 and len(tempRHS) > 0:
            temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' <= 1;'
            #print(temp)
            ampl.eval(temp)
            ind += 1
        
""" Constraint (v) """
tempLHS = ''
H = [(a, b) for (a, b) in g.edges if b == t]
#print(H)
for (a, b) in H:
    tempLHS += 'x[' + str(xEdges.index((a, b)) + 1) + '] + '
temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' = 1;'
#print(temp)
ampl.eval(temp)
ind += 1

""" Constraint (vi) """
tempLHS = ''
T = [(a, b) for (a, b) in g.edges if a == s]
#print(T)
for (a, b) in T:
    tempLHS += 'x[' + str(xEdges.index((a, b)) + 1) + '] + '
temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' = 2;'
#print(temp)
ampl.eval(temp)
ind += 1

""" Constraint (vii) """
for (a, b) in g.edges:
	temp = 'subject to const' + str(ind) + ': x[' + str(xEdges.index((a, b)) + 1) + '] * (1 - x[' + str(xEdges.index((a, b)) + 1) + ']) = 0;'
	ampl.eval(temp)
	ind += 1

""" Cut (i) """
if useCuts:
    for i in range(n):
        if i != s and i != t:
            H = [(a, b) for (a, b) in g.edges if b == i]
            T = [(a, b) for (a, b) in g.edges if a == i]
            #print(str(i + 1))
            #print(H)
            #print(T)
            tempLHS = ''
            tempRHS = ''
            for (c, d) in H:
                for ((a, b), (x, y)) in wEdges:
                    if x == c and y == d:
                        tempLHS += 'w[' + str(wEdges.index(((a, b), (c, d))) + 1) + '] + '
            for (c, d) in T:
                for ((a, b), (x, y)) in wEdges:
                    if x == c and y == d:
                        tempLHS += 'w[' + str(wEdges.index(((a, b), (c, d))) + 1) + '] + '
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

print("AMPL took " + str(time.time() - buildTime) + " seconds to build model!")

#ampl.eval('subject to (i) {e in 1..' + len(g.edges) + '}: sum {p in PATTERNS} rolls[w,p]* Cut[p]<= order[w]+ overrun;')
ampl.setOption('solver', 'baron')
ampl.setOption('baron_options', 'maxtime 3600')
#ampl.setOption('solver', 'gurobi')
#ampl.setOption('gurobi_options', 'NonConvex 2')
#ampl.setOption('cplex_options', 'iisfind 1')
startTime = time.time()
ampl.solve()
print("ampl.solve() took " + str(time.time() - startTime) + " seconds!")
#ampl.eval('display _varname, _var.iis, _conname, _con.iis;')
totalCost = ampl.getObjective('totalCost')
print("Objective is:", totalCost.value())
"""v = ampl.getVariable('v')
x = ampl.getVariable('x')
#w = ampl.getVariable('w')
print("v is:", v.getValues())
vVals = [0.0 for i in range(n)]
for vIndex, vVal in v.getValues():
    vVals[int(vIndex) - 1] = float(vVal)
print("x is:", x.getValues())
xVals = [0.0 for i in range(len(g.edges))]
for xIndex, xVal in x.getValues():
    xVals[int(xIndex) - 1] = float(xVal)

dot = Digraph(comment='Test', strict = True)

colors = ['blue', 'red', 'sienna', 'green', 'yellow']

for i in range(n):
    dot.node(str(i + 1), color=colors[0], style='filled')
for (a, b) in xEdges:
    if xVals[xEdges.index((a, b))] >= 0.900001:
        dot.edge(str(a + 1), str(b + 1), color=colors[0])#, style='filled')
        #dot.node(str(b + 1), color=colors[0], style='filled')
        #if (a, b) not in subgraph[0] and (a, b) not in subgraph[1] and (a, b) not in subgraph[2] and (a, b) not in subgraph[3]:
    else:
        dot.edge(str(a + 1), str(b + 1), color='black', style='dashed')
   
dot.render('test-output/round-table5.gv', view=True, format='png')"""
