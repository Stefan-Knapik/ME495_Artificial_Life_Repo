import pickle

f = open("BestSolution.obj", "rb")
BestSolution = pickle.load(f)
f.close()

BestSolution.Start_Simulation("GUI")