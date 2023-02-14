# Assignment 6
ME495 Artificial Life course at Northwestern University, which utilizes content from the r/ludobots evolutionary robotics subreddit.
https://www.reddit.com/r/ludobots/

## Generate Random 1D Creature Morphologies
This branch explores the generation of random creature morphologies. Random parameters include:
- number of body segments
- shape of body segments (box or cylinder)
- size of body segments
- joint directions (parallel to y or z)
- sensation (green links "feel", blue links are "numb")

## Running the code (Windows)
- Run __showRandom.py__ to generate and visualize a sequence of random creature morphologies.
- Simulation hyperparameters, including maximum joint forces and angles, can be set in __constants.py__
- Random morphology generation hyperparameters, such as the distributions of link number, size, and shape, can be set in the initialization of the SOLUTION class defined in __solution.py__