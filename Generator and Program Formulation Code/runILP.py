import os

for i in range(25):
    for j in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        os.system("python pathILP.py " + str(j) + " -1 0.1 >> Paths_ILP/random_" + str(j) + "_0.1.txt")
        os.system("python pathILP.py " + str(j) + " -1 0.2 >> Paths_ILP/random_" + str(j) + "_0.2.txt")
        os.system("python pathILP.py " + str(j) + " -1 0.3 >> Paths_ILP/random_" + str(j) + "_0.3.txt")
        os.system("python pathILP.py " + str(j) + " -1 0.4 >> Paths_ILP/random_" + str(j) + "_0.4.txt")
        os.system("python pathILP.py " + str(j) + " -1 0.5 >> Paths_ILP/random_" + str(j) + "_0.5.txt")
        os.system("python pathILP.py " + str(j) + " 2 0.1 >> Paths_ILP/ladder_" + str(j) + "_0.1.txt")
        os.system("python pathILP.py " + str(j) + " 3 0.1 >> Paths_ILP/circular_" + str(j) + "_0.1.txt")
        os.system("python pathILP.py " + str(j) + " 4 0.1 >> Paths_ILP/bipartite_" + str(j) + "_0.1.txt")
        os.system("python pathILP.py " + str(j) + " 6 0.1 >> Paths_ILP/wheel_" + str(j) + "_0.1.txt")