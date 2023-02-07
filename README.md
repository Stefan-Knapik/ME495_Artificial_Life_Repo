# ME495_Artificial Life Assignment 5

## Roly Pollie Robot Evolution

### Observed Behavior
These robots can roll, gallop, walk, jump, or crawl like an inchworm. Their emergent behavior depends on the strength, flexibility, and number of body segments we choose to grant them.

### Body Morphology
Body links are generated to form a regular n-sided polygon that circumscribes a circle in the x-z plane, where n > 3. Adjacent links are connected via revolute joints to form a broken hoop.
 
### Optimization
The objective function for minimization is still the final x-location of the root link.

Genetic crossover is implemented. Children "brains" are spawned through random generation, direct copy, or crossover between two parents according to a user defined reproduction distribution. Then they are mutated, and selection can be prescribed to occur within lineages, as with the parallel hill climber, or across the entire parent-child population.

## Running the code (in Windows)
Hyperparameters can be modified in **constant.py**
Evolutionary optimization can be performed by running **search.py**, which will display the best solution upon completion.

The best solution, saved from the last run of **search.py**, can be played again by running **BestVisualize.py**. Note: this visualization is still dependent on the current version of **constants.py**

### Future Plans
Crossover has sped up the optimization process, particularly for design spaces with many degrees of freedom (which currently scales with the square of the number of links).

However, the addition of genetic crossover can lead to a pretty homogenous population depending on the reproduction hyperparameters, because right now the most fit individuals are never eliminated from the population. This procedure is still prone to get stuck in local optima, just like the parallel hill climber. To mitigate this, I hope to implement a variant of the referenced age-fitness pareto optimization algorithm, which provides a mechanicsm for old and stagnant genes to die off even if they perform well. 
https://dl.acm.org/doi/pdf/10.1145/1830483.1830584?casa_token=tw1Py6GYT0oAAAAA:7yCJGlkaRLzpoYSN7UUPra7STN8QAjK2-eS5k1MOjOmLnqcyKdi52FiNhGckxodGG1Wgs0tO6JMJog


 
