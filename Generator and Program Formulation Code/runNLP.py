import os

for i in range(25):
    os.system("python pathNLP.py 10 -1 0.1 >> Paths_NLP/random_10_0.1.txt")
    os.system("python pathNLP.py 10 -1 0.2 >> Paths_NLP/random_10_0.2.txt")
    os.system("python pathNLP.py 10 -1 0.3 >> Paths_NLP/random_10_0.3.txt")
    os.system("python pathNLP.py 10 -1 0.4 >> Paths_NLP/random_10_0.4.txt")
    os.system("python pathNLP.py 10 -1 0.5 >> Paths_NLP/random_10_0.5.txt")
    os.system("python pathNLP.py 10 4 0.1 >> Paths_NLP/bipartite_10_0.1.txt")
    os.system("python pathNLP.py 10 6 0.1 >> Paths_NLP/wheel_10_0.1.txt")
    for j in [10, 20]:
        os.system("python pathNLP.py " + str(j) + " 2 0.1 >> Paths_NLP/ladder_" + str(j) + "_0.1.txt")
        os.system("python pathNLP.py " + str(j) + " 3 0.1 >> Paths_NLP/circular_" + str(j) + "_0.1.txt")
