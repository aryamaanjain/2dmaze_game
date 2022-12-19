# 2D Maze Game (OpenGL)
Aryamaan Jain  

## 1. To run code

* Run command `python3 Main.py`. 
* This project was done in python using `PyOpenGL`. To install `PyOpenGL` run command `pip install PyOpenGL PyOpenGL_accelerate`.
* This project uses `glut`.

## 2. Controls

1. `LEFT_ARROW`: Move player left
2. `RIGHT_ARROW`: Move player right
3. `UP_ARROW`: Move player up
4. `DOWN_ARROW`: Move player down
5. `ESC`: Quit game
6. `z`: Zoom-in
7. `x`: Zoom-out

## 3. Objects in game by color

1. Green: Player
2. Red: Enemy
3. Magenta: Obstacle
4. Yellow: Battery
5. Cyan: Score powerup
6. Blue: Health powerup

## 4. Game instructions

1. To win game, reach the bottommost leftmost cell. That cell contains the exit.
2. Avoid enemy, if caught health goes to 0.
3. Score health and battery are displayed in the bottom of the screen.
4. Brightness of lamp reduces with reduction of battery until pitch dark.
5. Obstacles do variable damage to health. Damage ranges from 1 to 3.
6. One scoreup gives one score point.
7. One battery gives one battery.
8. One healthup adds one to health.

## 5. Files in submission

1. `Enemy.py`: Contains class to handle enemy.
2. `Main.py`: Contains main code and most of opengl.
3. `Obstacles.py`: Contains classes to handle obstacles.
4.  `Player.py`: Contains class to handle player.
5. `Powerups.py`: Contains classes to handle powerups including battery, scoreup and healthup.
6. `Scoreboard.py`: Contains class to handle and display score and powerups.
7. `World.py`: Contains classes to handle the world. This includes making the grid and shadows.

## 6. Algorithms

### 6.1. Maze generation

Maze generation was done using backtracking. This was followed from the following website [link](https://thecodingtrain.com/CodingChallenges/010.1-maze-dfs-p5.html) by *The Coding Train*. Pseudocode can be found in Wikipedia [link](https://en.wikipedia.org/wiki/Maze_generation_algorithm). Pseudo-code is given below:

1. Choose the initial cell, mark it as visited and push it to the stack
2. While the stack is not empty
   1. Pop a cell from the stack and make it a current cell
   2. If the current cell has any neighbours which have not been visited
      1. Push the current cell to the stack
      2. Choose one of the unvisited neighbours
      3. Remove the wall between the current cell and the chosen cell
      4. Mark the chosen cell as visited and push it to the stack

### 6.2. Shadows

Shadows were generated using mask. 8 neighbours(4 immediate + 4 diagonal) were checked using condition where light can reach. The rest were masked with a black roof giving the impression of shadows and blocking light from going through walls.

### 6.3. Enemy movement

Enemy was moved towards the player by calculating a vector from enemy to player and sending the enemy in that direction. To prevent enemy from being stuck, some condition were applied such as if there is a wall in players direction then don't go there, instead got the other direction. For more safety of not getting stuck, some random movement was added to enemy.

### 6.4. Score

Scoring was done as per the number of scoreups a player could get.

## 7. Other information

1. FPS of game was kept 60.
2. The player starts from topmost rightmost cell.
3. After end of game, final results are printed in terminal.
