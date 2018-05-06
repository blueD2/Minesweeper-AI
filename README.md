## Minesweeper-AI
Game AI to play minesweeper using neuroevolution for Freshman Research Initiative group project

# Methodology
We used 24 inputs that represented a 5x5 border region around one cell. Each input was one of the following: -4 for bombs, -3 for walls, -1 for unknown, -2 for flags, and the "hint" numbers if shown. We chose these numbers based on a rough idea that higher surrounding values meant the square should be less likely to be clicked. We tried a couple different structures for the ANN, and we finally settled on a network with two hidden layers, the first with 15 hidden nodes and the second with 8 hidden nodes. The output layer was a single node denoting the probability of a cell being a bomb, a sort of "danger threshold" we used to determine if we should flag or click on that cell.

We used a population size of 100 and ran the algorithm for 100 generations, with a mutation probability of 0.3 and crossover probability of 0.3. Our game was an easy level, with a 10x10 board and 10 mines. For each generation, we had each neural network play the game until it died. This was accomplished by looping through all 100 cells, recording the highest and lowest probability, and using that to either flag or reveal one cell per turn. For each turn, if the highest value was over a 0.99 threshold and was closer to 1 than the lowest probability was to 0, then we flagged it as a likely bomb. Otherwise, we clicked the cell with the lowest danger probability. 

# Results
Our minesweeper AI definitely improved, especially near the beginning, and even won the game a couple of times, but we weren't able to produce this result consistently. This is probably due to the fact that minesweeper is a game highly based on luck, and one wrong move may result in instant death. Further improvements might be made in using the one-hot representation for our inputs instead of assigning our own values to bombs, walls, and flags, but that would have increased our number of inputs tenfold. We tried a couple different ways to calculate the score, combining correct flags, incorrect flags, and clear space, but there might have been a more optimal way to calculate it. In addition, we had no mechanism to unflag cells once they were flagged; instead, we just capped the number of flags at 10, which might have been a weakness of our implementation. Overall, we evolved ANNs that were able to get 50-70% of the flags most of the time.

# References
We adapted our Minesweeper game from here: https://gist.github.com/mohd-akram/3057736
