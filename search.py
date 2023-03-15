from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c

for i in range(1, c.trials+1):
    
    i = 4
    # Initialize parallel hill climber
    phc = PARALLEL_HILL_CLIMBER(random_seed=i)
    # Search for best robot
    phc.Evolve()
    
    # Show best robot
    # phc.Show_Best()
    
    # Initialize parallel hill climber with modified age-fitness pareto strategy
    phc = PARALLEL_HILL_CLIMBER(random_seed=i, algo='AFPO')
    # Search for best robot
    phc.Evolve()
    