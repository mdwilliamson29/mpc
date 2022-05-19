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

"""stronglyConnected = False
while not stronglyConnected:
    g = erdos_renyi_graph(n, p, directed=True)
    stronglyConnected = networkx.is_strongly_connected(g)"""
    
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
epsilon = 1e-6 #float(sys.argv[3]) #1e-5
optTolerance = 1e-9 #float(sys.argv[4]) #1e-6
feasTolerance = 1e-9 #float(sys.argv[5]) #1e-6
intTolerance = 1e-8 #float(sys.argv[6]) #1e-5; apparently should be greater than feasTolerance

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
			sign = random.randint(0, 1)
			value = random.randint(0, n)
			cost.append(sign * value + (sign - 1) * value)
			indexNum += 1

"""for (c, d) in [(a2, b2) for (a2, b2) in xEdges if a2 == s]:
    wIndices.append('w((0, 0), ({0}, {1}))'.format(c, d))
    #wIndices.append(indexNum)
    wEdges.append(((0, 0), (c, d)))
    cost.append(xCost[xEdges.index((c, d))]) # Is this correct?
    indexNum += 1"""

#print("xIndices")
#print(xIndices)
#print("wIndices")
#print(wIndices)

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
ampl.eval('maximize totalCost: sum {p in 1..' + str(n) + '} x[p];')

ind = 0

""" Constraint (i) """
for (a, b) in [(a2, b2) for (a2, b2) in xEdges if b2 != s]:
    #ampl.eval('subject to const' + str(ind) + ': 0 <= v[1] <= 1;')
    temp = 'subject to const' + str(ind) + ': v[' + str(b + 1) + '] >= v[' + str(a + 1) + '] + ' + str(n + 1) + ' * x[' + str(xEdges.index((a, b)) + 1) + '] - ' + str(n) + ';'
    #print(temp)
    ampl.eval(temp)
    ind += 1

""" Constraint (i) """
"""for (a, b) in [(a2, b2) for (a2, b2) in xEdges if b2 != s]:
    #ampl.eval('subject to const' + str(ind) + ': 0 <= v[1] <= 1;')
    temp = 'subject to const' + str(ind) + ': v[' + str(b + 1) + '] >= v[' + str(a + 1) + '] + ' + str(n + 1) + ' * x[' + str(xEdges.index((a, b)) + 1) + '] - ' + str(n) + ';'
    print(temp)
    ampl.eval(temp)
    ind += 1"""

""" Constraint (ii) """
for ((a, b), (c, d)) in wEdges:
    if (a, b) != (0, 0):
        temp = 'subject to const' + str(ind) + ': x[' + str(xEdges.index((a, b)) + 1) + '] + x[' + str(xEdges.index((c, d)) + 1) + '] - 1 <= w[' + str(wEdges.index(((a, b), (c, d))) + 1) + '];'
        #print(temp)
        ampl.eval(temp)
        ind += 1

""" Constraint (iii) """
"""for (c, d) in [(a2, b2) for (a2, b2) in xEdges if a2 == s]:
    temp = 'subject to const' + str(ind) + ': w[' + str(wEdges.index(((0, 0), (c, d))) + 1) + '] = x[' + str(xEdges.index((c, d)) + 1) + '];'
    #print(temp)
    ampl.eval(temp)
    ind += 1"""

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
	""" Constraint (vi) """
	if len(tempLHS) > 0 and len(tempRHS) > 0:
		temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' <= 1;'
		#print(temp)
		ampl.eval(temp)
		ind += 1
        
""" Constraint (vii) """
ampl.eval('subject to const' + str(ind) + ': sum {p in 1..' + str(len(wEdges)) + '} cost[p] * w[p] <= -1;')
ind += 1




#ampl.eval('subject to (i) {e in 1..' + len(g.edges) + '}: sum {p in PATTERNS} rolls[w,p]* Cut[p]<= order[w]+ overrun;')
ampl.setOption('solver', 'cplex')
#ampl.setOption('cplex_options', 'iisfind 1')
startTime = time.time()
ampl.solve()
print("ampl.solve() took " + str(time.time() - startTime) + " seconds!")
#ampl.eval('display _varname, _var.iis, _conname, _con.iis;')
totalCost = ampl.getObjective('totalCost')
print("Objective is:", totalCost.value())



print("Using Cuts")


buildTime = time.time()

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
                    tempRHS += 'w[' + str(wEdges.index(((a, b), (c, d))) + 1) + '] + '
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
        """ Constraint (???) """
        if len(tempLHS) > 0 and len(tempRHS) > 0:
            temp = 'subject to const' + str(ind) + ': ' + tempLHS[:-3] + ' <= 1;'
            #print(temp)
            ampl.eval(temp)
            ind += 1

#print("AMPL took " + str(time.time() - buildTime) + " seconds to build model!")

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




"""v = ampl.getVariable('v')
x = ampl.getVariable('x')
w = ampl.getVariable('w')
#print("v is:", v.getValues())
vVals = [0 for i in range(n)]
for vIndex, vVal in v.getValues():
    vVals[int(vIndex) - 1] = int(vVal)
#print("x is:", x.getValues())
xVals = [0 for i in range(len(g.edges))]
for xIndex, xVal in x.getValues():
    xVals[int(xIndex) - 1] = int(xVal)
#print("w is:", w.getValues())
wVals = [0 for i in range(len(wEdges))]
for wIndex, wVal in w.getValues():
    wVals[int(wIndex) - 1] = int(wVal)"""

#print("costs")
#for ((a, b), (c, d)) in wEdges:
#    print("(" + str(a + 1) + ", " + str(b + 1) + "), (" + str(c + 1) + ", " + str(d + 1) + ")): " + str(cost[wEdges.index(((a, b), (c, d)))]))

#print(sum(wVals))

"""dot = Digraph(comment='Test', strict = True)
#dot.rankdir = 'LR'
#dot.rotate = 90
#dot.orientation = 'landscape'
#dot.landscape = True

colors = ['blue', 'red', 'sienna', 'green', 'yellow']
#for (a, b) in graph:
#    dot.edge(str(a + 1), str(b + 1), color='black', style='dashed')
#ergStates = [j for sub in ergsets for j in sub]
for i in range(n):
    dot.node(str(i + 1)) #, color='white', style='filled')
for (a, b) in xEdges:
    if xVals[xEdges.index((a, b))] == 1:
        dot.edge(str(a + 1), str(b + 1), color=colors[0])#, style='filled')
        #dot.node(str(b + 1), color=colors[0], style='filled')
        #if (a, b) not in subgraph[0] and (a, b) not in subgraph[1] and (a, b) not in subgraph[2] and (a, b) not in subgraph[3]:
    else:
        dot.edge(str(a + 1), str(b + 1), color='black', style='dashed')
for ((a, b), (c, d)) in wEdges:
    if wVals[wEdges.index(((a, b), (c, d)))] == 1:
        dot.edge(str(a + 1), str(b + 1), color='red')#, style='filled')
        dot.edge(str(c + 1), str(d + 1), color='red', label=str(cost[wEdges.index(((a, b), (c, d)))]))
        #dot.node(str(b + 1), color=colors[0], style='filled')
        #if (a, b) not in subgraph[0] and (a, b) not in subgraph[1] and (a, b) not in subgraph[2] and (a, b) not in subgraph[3]:
    #else:
    #    dot.edge(str(a + 1), str(b + 1), color='black', style='dashed')
    #    dot.edge(str(c + 1), str(d + 1), color='black', style='dashed')
   
#dot.render('test-output/round-table5.gv', view=True, format='png')"""

"""
costs
(1, 2), (2, 1)): 2
(1, 2), (2, 3)): 1
(1, 2), (2, 4)): 4
(1, 3), (3, 1)): 3
(1, 3), (3, 2)): 2
(1, 4), (4, 3)): 4
(2, 1), (1, 2)): 2
(2, 1), (1, 3)): 3
(2, 1), (1, 4)): 0
(2, 3), (3, 1)): 0
(2, 3), (3, 2)): 2
(2, 4), (4, 3)): 1
(3, 1), (1, 2)): 2
(3, 1), (1, 3)): 1
(3, 1), (1, 4)): 4
(3, 2), (2, 1)): 1
(3, 2), (2, 3)): 1
(3, 2), (2, 4)): 0
(4, 3), (3, 1)): 0
(4, 3), (3, 2)): 1
(1, 1), (1, 2)): 0
(1, 1), (1, 3)): 3
(1, 1), (1, 4)): 3
"""

"""print(o)

#var Buy {j in FOOD} binary >= f_min[j], <= f_max[j];


# Interpret the two files
ampl.read('models/cut.mod')
ampl.readData('models/cut.dat')


# Solve
ampl.solve()

print(o)

# Get objective entity by AMPL name
totalcost = ampl.getObjective('total_cost')
# Print it
print("Objective is:", totalcost.value())

# Reassign data - specific instances
cost = ampl.getParameter('cost')
cost.setValues({'BEEF': 5.01, 'HAM': 4.55})
print("Increased costs of beef and ham.")

# Resolve and display objective
ampl.solve()
print("New objective value:", totalcost.value())

# Reassign data - all instances
cost.setValues([3, 5, 5, 6, 1, 2, 5.01, 4.55])

print("Updated all costs.")

# Resolve and display objective
ampl.solve()
print("New objective value:", totalcost.value())

# Get the values of the variable Buy in a dataframe object
buy = ampl.getVariable('Buy')
df = buy.getValues()
# Print them
print(df)

# Get the values of an expression into a DataFrame object
df2 = ampl.getData('{j in FOOD} 100*Buy[j]/Buy[j].ub')
# Print them
print(df2)"""

