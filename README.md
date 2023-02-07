# ME495_Artificial Life Assignment 5

## Roly Pollie Robot Evolution

### Observed Behavior
These robots can roll, gallop, walk, jump, or crawl like an inchworm. Their emergent behavior depends on the strength, flexibility, and number of body segments we choose to grant them.

### Body Morphology
Body links are generated to form a regular n-sided polygon that circumscribes a circle in the x-z plane, where n > 3. Adjacent links are connected via revolute joints to form a broken hoop.
 
### Optimization
The objective function for minimization is still the final x-location of the root link.

Genetic crossover is implemented. Children "brains" are spawned through random generation, direct copy, or crossover between two parents according to a user defined reproduction distribution. Then they are mutated, and selection can be prescribed to occur within lineages, as with the parallel hill climber, or across the entire parent-child population.

### Future Plans
The addition of genetic crossover can lead to a pretty homogenous population depending on the reproduction hyperparameters. I hope to incorporate

## Running the code (in Windows)
Hyperparameters can be modified in **constant.py**
Evolutionary optimization can be performed by running **search.py**, which will display the best solution upon completion.

The best solution, saved from the last run of **search.py**, can be played again by running **BestVisualize.py**. Note: this visualization is still dependent on the current version of **constants.py**
 
