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

"""stronglyConnected = False
while not stronglyConnected:
    g = erdos_renyi_graph(n, p, directed=True)
    stronglyConnected = networkx.is_strongly_connected(g)"""
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
	sign = random.randint(0, 1)
	value = random.randint(0, n)
	xCost.append(sign * value + (sign - 1) * value)
	indexNum += 1
	
wIndices = []
wEdges = []
cost = [[0.0 for j in range(len(g.edges))] for i in range(len(g.edges))]
sc = [[0 for j in range(len(g.edges))] for i in range(len(g.edges))]
indexNum = 0

xObj = []
for (a, b) in g.edges: 
	for (c, d) in g.edges:
		if b == c:
			wIndices.append('w(({0}, {1}), ({2}, {3}))'.format(a, b, c, d))
			#wIndices.append(indexNum)
			wEdges.append(((a, b), (c, d)))
			sign = random.randint(0, 1)
			value = random.randint(0, n)
			xObj.append((xEdges.index((a, b)), xEdges.index((c, d))))
			#cost.append(sign * value + (sign - 1) * value)
			cost[xEdges.index((a, b))][xEdges.index((c, d))] = sign * value + (sign - 1) * value
			sc[xEdges.index((a, b))][xEdges.index((c, d))] = 1
			indexNum += 1

buildTime = time.time()

ampl = AMPL()

ampl.eval('param cost {1..' + str(len(g.edges)) + ', 1..' + str(len(g.edges)) + '};')
costParam = ampl.getParameter('cost')
costParam.setValues([y for x in cost for y in x])
ampl.eval('var x{1..' + str(len(g.edges)) + '} >= 0, <= 1;')
ampl.eval('param sc {1..' + str(len(g.edges)) + ', 1..' + str(len(g.edges)) + '} >= 0;')
scParam = ampl.getParameter('sc')

"""sc = [[0 for j in range(len(g.edges))] for i in range(len(g.edges))]
for i in range(len(g.edges)):
	for j in range(len(g.edges)):
		if (i, j) in xObj:		
			sc[i][j] = 1"""

scParam.setValues([y for x in sc for y in x])
scParam = ampl.getParameter('sc')
ampl.eval('set rt := {d in 1..' + str(len(g.edges)) + ', w in 1..' + str(len(g.edges)) + ': sc[d, w] = 1};')

#ampl.eval('maximize totalCost: sum {p in 1..' + str(len(g.edges)) + '} x[p];')
ind = 0

""" Constraint (i) """
for (a, b) in g.edges:
	temp = 'subject to const' + str(ind) + ': x[' + str(xEdges.index((a, b)) + 1) + '] * (1 - x[' + str(xEdges.index((a, b)) + 1) + ']) = 0;'
	ampl.eval(temp)
	ind += 1

""" Constraint (ii) """
for i in range(n):
	H = [(a, b) for (a, b) in g.edges if b == i]
	T = [(a, b) for (a, b) in g.edges if a == i]
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
	""" Constraint (iii) """
	if len(tempLHS) > 0 and len(tempRHS) > 0:
		temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' <= 1;'
		#print(temp)
		ampl.eval(temp)
		ind += 1
        
""" Constraint (iv) """
ampl.eval('subject to const' + str(ind) + ': sum {(i, j) in rt} cost[i, j] * x[i] * x[j] <= -1;')

"""print("AMPL took " + str(time.time() - buildTime) + " seconds to build model!")

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
print("Objective is:", totalCost.value())"""


ampl.setOption('solver', 'baron')
ampl.setOption('baron_options', 'maxtime 3600')

print("NCCD")
ampl.eval('minimize totalCost: 0;')
startTime = time.time()
ampl.solve()
print("ampl.solve() took " + str(time.time() - startTime) + " seconds!")
#ampl.eval('display _varname, _var.iis, _conname, _con.iis;')
totalCost = ampl.getObjective('totalCost')
print("Objective is:", totalCost.value())
#v = ampl.getVariable('v')


print("SNCC")
ampl.eval('minimize totalCost_SNCC: sum {p in 1..' + str(len(g.edges)) + '} x[p];')
startTime = time.time()
ampl.solve()
print("ampl.solve() took " + str(time.time() - startTime) + " seconds!")
#ampl.eval('display _varname, _var.iis, _conname, _con.iis;')
totalCost = ampl.getObjective('totalCost_SNCC')
print("Objective is:", totalCost.value())


"""x = ampl.getVariable('x')
xVals = [0.0 for i in range(len(g.edges))]
for xIndex, xVal in x.getValues():
    xVals[int(xIndex) - 1] = float(xVal)

dot = Digraph(comment='Test', strict = True)
#dot.rankdir = 'LR'
#dot.rotate = 90
#dot.orientation = 'landscape'
#dot.landscape = True

colors = ['blue', 'red', 'sienna', 'green', 'yellow']
#for (a, b) in graph:
#    dot.edge(str(a + 1), str(b + 1), color='black', style='dashed')
#ergStates = [j for sub in ergsets for j in sub]
for i in range(n):
    dot.node(str(i + 1)) #, color=colors[0], style='filled')
for (a, b) in xEdges:
    if xVals[xEdges.index((a, b))] > 0.9:
        dot.edge(str(a + 1), str(b + 1), color=colors[0])#, style='filled')
        #dot.node(str(b + 1), color=colors[0], style='filled')
        #if (a, b) not in subgraph[0] and (a, b) not in subgraph[1] and (a, b) not in subgraph[2] and (a, b) not in subgraph[3]:
    else:
        dot.edge(str(a + 1), str(b + 1), color='black', style='dashed')
   
dot.render('test-output/round-table5.gv', view=True, format='png')"""
