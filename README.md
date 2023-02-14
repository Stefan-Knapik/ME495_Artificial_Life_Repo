# Assignment 6
ME495 Artificial Life course at Northwestern University, which utilizes content from the r/ludobots evolutionary robotics subreddit.
https://www.reddit.com/r/ludobots/

## Generate random 1D creature morphologies
This branch of the repository explores the generation of random creature morphologies. Random parameters include:
- number of body segments
- shape of body segments (box or cylinder)
- size of body segments
- joint directions (parallel to y or z)
- sensation (green links "feel", blue links are "numb")

!<img src="https://user-images.githubusercontent.com/101603342/218656723-7c701f06-679c-4356-9591-0cd3550835a7.png" height="100">
!<img src="https://user-images.githubusercontent.com/101603342/218656777-4b86f993-9b94-4784-bff9-a6b91dcba712.png" height="100" />
!<img src="https://user-images.githubusercontent.com/101603342/218656802-b000b42e-e5c9-4cb6-be5f-613b62869d14.png" height="100" />
!<img src="https://user-images.githubusercontent.com/101603342/218656824-899005a0-72f5-437c-b905-07b20b8694ff.png" height="100" />




## Run the code (Windows)
Run __showRandom.py__ to generate and visualize a sequence of random creature morphologies.

- Simulation parameters, including maximum joint forces and angles, can be set in __constants.py__
- Random morphology generation parameters, such as the distributions of link number, size, and shape, can be set in the constructor of the SOLUTION class defined in __solution.py__
