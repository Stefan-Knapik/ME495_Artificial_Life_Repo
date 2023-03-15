# Final Project

## Summary
Here we explore the evolutionary optimization of 3-dimensional robots for locomotion. These robots have rigid and spherical body segments, sensors, and motors, and they can evolve to exhibit a variety of locomotion modes including what may be described as walking, jumping, galloping, or rolling.

YouTube Video: https://youtu.be/Scpsa_iSDLs

## Hypothesis
The performance of two optimization algorithms, a parallel hill climber and an age-fitness Pareto optimization scheme, are compared.

I suspect that the age-fitness Pareto optimization algorithm will be able to find better designs than the parallel hill climber for a given simulation budget because the parallel hill climber has no mechanism to escape local optima that members of its population may settle into.

## Body Generation
Robots are initially generated randomly according to the following variable parameters.
- number of spherical body segments
- size of each body segment
- joint locations with respect to parent links
- joint axis directions
- sensation (green links "feel", blue links are "numb")
- maximum number of children per link constraint
- maximum depth of the link tree constraint

<img src="https://user-images.githubusercontent.com/101603342/220268996-d46b12c3-8011-4e0b-941c-9acd234cd08e.png" height="150"
img src="https://user-images.githubusercontent.com/101603342/220268996-d46b12c3-8011-4e0b-941c-9acd234cd08e.png" height="150" />
<img src="https://user-images.githubusercontent.com/101603342/220269218-7c00e2d5-df58-4e8b-8b6f-c8db53be3de5.png" height="150" />
<img src="https://user-images.githubusercontent.com/101603342/220269318-3275684b-3892-4ffd-8a16-16e25d6c50de.png" height="150" />
<img src="https://user-images.githubusercontent.com/101603342/220269447-df648bc3-5b17-4d87-b228-af66d73ce344.png" height="150" />

Here we limit ourselves to spherical body segments for the sake of simple collision detection during body generation. While the default simulation parameters will allow links to intersect as they move, ensuring that links do not initially intersect assures us that we can simulate these robots with global collision detection if we so choose.

**Number of links**, **maximum children per link**, and **maximum link tree depth** are randomly prescribed for each robot. **Link radius** is uniformly randomly selected for each link. **Joint locations** and **Joint axis directions** are uniformly randomly tried over the spherical link surfaces via some fun math (search spherically symmetric distributions to learn more!) until a collision-free structure is achieved. Link **sensation** occurs at a fixed probability over all the links.

### Body Initialization Procedure
1. Create the root link at a specified location.
2. Randomly choose an existing link that is eligible to have a child. Links can be disqualified from further parenthood if they have too many children or are too deep in the tree.
3. Propose a random joint (location and direction) and link (size and sensation) to stem from the chosen parent.
4. If spawning this new joint-link pair will create a collision with the floor or other links, go back to Step 2.
5. Accept the randomly generated joint-link pair.
6. Repeat from Step 2 until the number of links is satisfied.

![image](https://user-images.githubusercontent.com/101603342/220275338-f7aedc9c-7b06-425b-9f80-417416bdb1ad.png)

### Genetic Representation

## Run the code (on Windows)
Run __showRandom.py__ to generate and visualize a sequence of random creature morphologies.

- Simulation parameters, including maximum joint forces and angles, can be set in __constants.py__
- Random morphology generation parameters can be set in the constructor of the SOLUTION class defined in __solution2.py__

If simulating with global collision detection, the "connect_factor" variable in __solution2.py__ should be set slightly greater than 1 to ensure joint mobility. With a value of 1, the links are exactly touching without collision. The default value is 0.9 for aesthetic purposes, which is unproblematic for simulation without self-collision.

## Evolve morphology and behavior concurrently (using a parallel hill climber)
This branch of the repository explores the genetic optimization of creature morphologies and behaviors for locomotion in the negative x-direction.

The random design initializations follow the same strategy as the branch for assignment 7.

https://github.com/Stefan-Knapik/ME495_Artificial_Life_Repo/tree/HW7-Random3D

For the genetic algorithm, a variety of random mutations are permitted to occur according to a user-defined probability distribution. These include changes that only affect the "brain", only affect the "body", or require modification to both simultaneously. The scope of each type of mutation is summarized below:
- single neuron weight
- sensor swap
- motor swap
- add/remove a sensor
- joint axis direction
- add a body segment
- remove a body segment (currently only implemented for leaf links)
- resize a body segment
- joint location (implemented but unused, needs further work to avoid breaking the rules of Assignment 7)

Governing parameters are adjustable, and it is noted that most of the robots shown in the YouTube video were initialized with few body segments and allowed to "grow" as they evolved. This harnesses the synergistic advantage of evolving behavior and body together, rather than starting with a large body and randomly (hopelessly?) searching a massive behavior space from scratch.

Below is an image depicting the progression of fitness through 5 different evolving populations.

<img src="https://user-images.githubusercontent.com/101603342/222029673-3fe8d92c-287e-42f3-91f3-f10a14b3ce61.png" width="600" />

## Run the code (Windows)

Ensure all of the files from this repository are present in your working directory (e.g., by cloning this repository or downloading it as a ZIP file).

Run __search.py__ to use a parallel hill climber to genetically optimize robots for locomotion in the negative x-direction.

- Simulation parameters, including maximum joint forces and angles, can be set in __constants.py__
- Random morphology generation parameters can be set in the constructor of the SOLUTION class defined in __solution.py__

__BestVisualize.py__ serves to easily visualize optimized creatures.
__PlotFitness.py__ will generate a plot comparable to the one above (after having previously run __search.py__).

If simulating with global collision detection, the "connect_factor" variable in __solution.py__ should be set slightly greater than 1 to ensure joint mobility. With a value of 1, the links are exactly touching without collision. The default value is 0.99 for aesthetic purposes, which is unproblematic for simulation without self-collision.

## References

Bongard, J. “Education in Evolutionary Robotics” Reddit, https://www.reddit.com/r/ludobots/.

Bongard, J. pyrosim GitHub repository, https://github.com/jbongard/pyrosim.

Coumans, E., Bai, Y., and Hsu, J. pybullet Python module for physics simulation

Kriegman, S. Artificial Life Course, Northwestern University, Evanston, Illinois, Winter 2023.

Schmidt, M., and Lipson H. “Age-Fitness Pareto Optimization.” Genetic Programming Theory and Practice VIII, 2010, pp. 129–146., https://doi.org/10.1007/978-1-4419-7747-2_8. 
