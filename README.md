# Assignment 8
ME495 Artificial Life course at Northwestern University, which utilizes content from the r/ludobots evolutionary robotics subreddit.
https://www.reddit.com/r/ludobots/

## YouTube Video
https://youtu.be/Scpsa_iSDLs

## Evolve morphology and behavior concurrently (using a parallel hill climber)
This branch of the repository explores the genetic optimization of creature morphologies and behaviors. 

The random design initializations follow the same strategy as the repository for assignment 7.

https://github.com/Stefan-Knapik/ME495_Artificial_Life_Repo/tree/HW7-Random3D

For the genetic algorithm, a variety of random mutations are permitted to occur according to a user-defined probability distribution. These include changes that only affect the "brain", only affect the "body", or require modification to both simultaneously. The scope of each type of mutation is summarized below:
-single neuron 
-sensor swap
-motor swap
-add/remove a sensor
-joint axis direction
-add a body segment
-remove a body segment (currently only implemented for leaf links)
-resize a body segment
-joint location (implemented but unused, needs further work to avoid breaking the rules of Assignment 7)

Hyperparameters are adjustable, but it is noted that most of the robots shown in the YouTube video were initialized with few body segments, and allowed to "grow" as they evolved to encourage the synergistic advantage of evolving behavior and body together, rather than starting with a large body and randomly searching a massive behavior space from scratch.

Below is an image depicting the progression of fitness through 5 different evolving populations.

<img src="https://user-images.githubusercontent.com/101603342/222029673-3fe8d92c-287e-42f3-91f3-f10a14b3ce61.png" width="150" />


## Run the code (Windows)
Run __search.py__ to use a parallel hill climber to genetically optimize robots for locomotion in the negative x-direction.

- Simulation parameters, including maximum joint forces and angles, can be set in __constants.py__
- Random morphology generation parameters can be set in the constructor of the SOLUTION class defined in __solution.py__

Run __BestVisualize.py__ serves to easily display optimized creatures.
Run __PlotFitness.py__ will generate a plot comparable to the one above (after having run __search.py__).

If simulating with global collision detection, the "connect_factor" variable in __solution2.py__ should be set slightly greater than 1 to ensure joint mobility. With a value of 1, the links are exactly touching without collision. The default value is 0.99 for aesthetic purposes, which is unproblematic for simulation without self-collision.
