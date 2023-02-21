# Assignment 7
ME495 Artificial Life course at Northwestern University, which utilizes content from the r/ludobots evolutionary robotics subreddit.
https://www.reddit.com/r/ludobots/

## Generate random 3D creature morphologies
This branch of the repository explores the generation of random creature morphologies. Random parameters include:
- number of spherical body segments
- size of the body segments
- joint locations
- joint axis directions
- sensation (green links "feel", blue links are "numb")
- maximum number of children per link
- maximum depth of the link tree

<img src="https://user-images.githubusercontent.com/101603342/220268996-d46b12c3-8011-4e0b-941c-9acd234cd08e.png" height="150"
img src="https://user-images.githubusercontent.com/101603342/220268996-d46b12c3-8011-4e0b-941c-9acd234cd08e.png" height="150" />
<img src="https://user-images.githubusercontent.com/101603342/220269218-7c00e2d5-df58-4e8b-8b6f-c8db53be3de5.png" height="150" />
<img src="https://user-images.githubusercontent.com/101603342/220269318-3275684b-3892-4ffd-8a16-16e25d6c50de.png" height="150" />
<img src="https://user-images.githubusercontent.com/101603342/220269447-df648bc3-5b17-4d87-b228-af66d73ce344.png" height="150" />

Here we limit ourselves to spherical body segments for the sake of simple collision detection during body generation. While the default simulation parameters will allow links to intersect as they move, ensuring that links do not initially intersect assures us that we can simulate these robots with global collision detection if we so choose.

**Number of links**, **maximum children per link**, and **maximum link tree depth** are prescribed for each robot. **Link radius** is uniformly randomly chosen for each link. **Joint locations** are uniformly randomly tried over the spherical link surfaces via some fun math (search spherically symmetric distributions to learn more)! **Joint axis directions** are uniformly randomly generated, but constrained to be tangential to the spherical link surfaces. Link **sensation** occurs at a fixed probability over all the links.

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
