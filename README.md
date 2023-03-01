# Assignment 8
ME495 Artificial Life course at Northwestern University, which utilizes content from the r/ludobots evolutionary robotics subreddit.
https://www.reddit.com/r/ludobots/

## YouTube Video
https://youtu.be/Scpsa_iSDLs

## Evolve morphology and behavior concurrently (using a parallel hill climber)
This branch of the repository explores the genetic optimization of creature morphologies and behaviors. 

The random design initializations follow the same strategy as the repository for assignment 7.
https://github.com/Stefan-Knapik/ME495_Artificial_Life_Repo/tree/HW7-Random3D


Here we limit ourselves to spherical body segments for the sake of simple collision detection during body generation. While the default simulation parameters will allow links to intersect as they move, ensuring that links do not initially intersect assures us that we can simulate these robots with global collision detection if we so choose.

**Number of links**, **maximum children per link**, and **maximum link tree depth** are prescribed for each robot. **Link radius** is uniformly randomly chosen for each link. **Joint locations** are uniformly randomly tried over the spherical link surfaces via some fun math (search spherically symmetric distributions to learn more)! **Joint axis directions** are uniformly randomly generated, but constrained to be tangential to the spherical link surfaces. Link **sensation** occurs at a fixed probability over all the links.

Note: If the maximum number of children per link is prescribed as 1, this project degenerates to a 1D case suitable for Assignment 6.

## Procedure
1. Create the root link at a specified location.
2. Randomly choose an existing link that is eligible to have a child. Links can be disqualified from further parenthood if they have too many children or are too deep in the tree.
3. Propose a random joint and link to stem from the chosen parent.
4. If spawning this new joint-link pair will create a collision with the floor or other links, go back to Step 2.
5. Accept the randomly generated joint-link pair.
6. Repeat from Step 2 until the number of links is satisfied.

![image](https://user-images.githubusercontent.com/101603342/220275338-f7aedc9c-7b06-425b-9f80-417416bdb1ad.png)

## Run the code (Windows)
Run __showRandom.py__ to generate and visualize a sequence of random creature morphologies.

- Simulation parameters, including maximum joint forces and angles, can be set in __constants.py__
- Random morphology generation parameters can be set in the constructor of the SOLUTION class defined in __solution2.py__

If simulating with global collision detection, the "connect_factor" variable in __solution2.py__ should be set slightly greater than 1 to ensure joint mobility. With a value of 1, the links are exactly touching without collision. The default value is 0.9 for aesthetic purposes, which is unproblematic for simulation without self-collision.
