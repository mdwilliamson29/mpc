import os

for i in range(20):
    for j in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        os.system("python longestCycleNLP.py " + str(j) + " -1 0.1 >> longestCycleNLP/random_" + str(j) + "_0.1.txt")
        os.system("python longestCycleNLP.py " + str(j) + " -1 0.2 >> longestCycleNLP/random_" + str(j) + "_0.2.txt")
        os.system("python longestCycleNLP.py " + str(j) + " -1 0.3 >> longestCycleNLP/random_" + str(j) + "_0.3.txt")
        os.system("python longestCycleNLP.py " + str(j) + " -1 0.4 >> longestCycleNLP/random_" + str(j) + "_0.4.txt")
        os.system("python longestCycleNLP.py " + str(j) + " -1 0.5 >> longestCycleNLP/random_" + str(j) + "_0.5.txt")
        os.system("python longestCycleNLP.py " + str(j) + " 2 0.1 >> longestCycleNLP/ladder_" + str(j) + "_0.1.txt")
        os.system("python longestCycleNLP.py " + str(j) + " 3 0.1 >> longestCycleNLP/circular_" + str(j) + "_0.1.txt")
        os.system("python longestCycleNLP.py " + str(j) + " 4 0.1 >> longestCycleNLP/bipartite_" + str(j) + "_0.1.txt")
        os.system("python longestCycleNLP.py " + str(j) + " 6 0.1 >> longestCycleNLP/wheel_" + str(j) + "_0.1.txt")