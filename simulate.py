from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = int(sys.argv[2])

simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.GET_FITNESS()


