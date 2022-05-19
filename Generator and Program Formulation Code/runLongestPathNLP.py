import os

#Wheel 10
#Random 10 0.5
#Ladder 30
#Circular 20
#Bipartite 10

for i in range(20):
    os.system("python longestPathNLP.py 10 -1 0.1 >> longestPathNLP/random_10_0.1.txt")
    os.system("python longestPathNLP.py 10 -1 0.2 >> longestPathNLP/random_10_0.2.txt")
    os.system("python longestPathNLP.py 10 -1 0.3 >> longestPathNLP/random_10_0.3.txt")
    os.system("python longestPathNLP.py 10 -1 0.4 >> longestPathNLP/random_10_0.4.txt")
    os.system("python longestPathNLP.py 10 -1 0.5 >> longestPathNLP/random_10_0.5.txt")
    os.system("python longestPathNLP.py 20 -1 0.1 >> longestPathNLP/random_20_0.1.txt")
    os.system("python longestPathNLP.py 10 2 0.1 >> longestPathNLP/ladder_10_0.1.txt")
    os.system("python longestPathNLP.py 20 2 0.1 >> longestPathNLP/ladder_20_0.1.txt")
    os.system("python longestPathNLP.py 30 2 0.1 >> longestPathNLP/ladder_30_0.1.txt")
    os.system("python longestPathNLP.py 10 3 0.1 >> longestPathNLP/circular_10_0.1.txt")
    os.system("python longestPathNLP.py 20 3 0.1 >> longestPathNLP/circular_20_0.1.txt")
    os.system("python longestPathNLP.py 10 4 0.1 >> longestPathNLP/bipartite_10_0.1.txt")
    os.system("python longestPathNLP.py 10 6 0.1 >> longestPathNLP/wheel_10_0.1.txt")    

    """for j in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        os.system("python longestPathNLP.py " + str(j) + " -1 0.1 >> longestPathNLP/random_" + str(j) + "_0.1.txt")
        os.system("python longestPathNLP.py " + str(j) + " -1 0.2 >> longestPathNLP/random_" + str(j) + "_0.2.txt")
        os.system("python longestPathNLP.py " + str(j) + " -1 0.3 >> longestPathNLP/random_" + str(j) + "_0.3.txt")
        os.system("python longestPathNLP.py " + str(j) + " -1 0.4 >> longestPathNLP/random_" + str(j) + "_0.4.txt")
        os.system("python longestPathNLP.py " + str(j) + " -1 0.5 >> longestPathNLP/random_" + str(j) + "_0.5.txt")
        os.system("python longestPathNLP.py " + str(j) + " 2 0.1 >> longestPathNLP/ladder_" + str(j) + "_0.1.txt")
        os.system("python longestPathNLP.py " + str(j) + " 3 0.1 >> longestPathNLP/circular_" + str(j) + "_0.1.txt")
        os.system("python longestPathNLP.py " + str(j) + " 4 0.1 >> longestPathNLP/bipartite_" + str(j) + "_0.1.txt")
        os.system("python longestPathNLP.py " + str(j) + " 6 0.1 >> longestPathNLP/wheel_" + str(j) + "_0.1.txt")"""