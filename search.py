from parallelHillClimber import PARALLEL_HILL_CLIMBER

for i in range(1,6):
    
    # Initialize parallel hill climber
    phc = PARALLEL_HILL_CLIMBER(random_seed=i)
    
    # Search for best robot
    phc.Evolve()
    
    # Show best robot
    # phc.Show_Best()
