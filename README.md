# 3D Car and Boy Game


https://github.com/user-attachments/assets/fe3567a6-2c7a-4647-a002-4c8c759dedd2






A simple 3D driving game built with Pygame and OpenGL where you control a car, avoid obstacles, and collect points.

## Description

This game uses Python with Pygame and PyOpenGL to create a 3D driving experience. Players control a red car on a road, avoiding obstacles while trying to achieve a high score. The game features simple but effective 3D graphics including trees, obstacles, and a boy character.

## Features

- 3D graphics rendered with OpenGL
- Car controls with keyboard input
- Obstacle avoidance gameplay
- Scoring system
- Randomly generated obstacles and scenery
- Simple but effective collision detection
- Game over and restart functionality

## Requirements

- Python 3.x
- Pygame
- PyOpenGL
- NumPy

## How to Play

- Use the **WASD** keys or **Arrow Keys** to control the car:
  - **W** or **Up Arrow**: Increase speed
  - **S** or **Down Arrow**: Decrease speed
  - **A** or **Left Arrow**: Move left
  - **D** or **Right Arrow**: Move right
- Avoid the brown obstacle boxes on the road
- Your score increases for each obstacle you successfully pass
- If you hit an obstacle, the game ends
- Press **R** to restart after game over

## Game Mechanics

- The car's speed increases or decreases based on player input
- Obstacles are randomly generated and placed on the road
- Trees are placed randomly on both sides of the road for scenery
- A boy character occasionally appears on the side of the road
- The score increases with each obstacle you pass
- The game over screen shows your final score

## Code Structure

The game is built around several key functions:
- Drawing primitives (cube, cylinder, sphere, cone)
- Object renderers for the car, boy, trees, and obstacles
- Game state management (obstacle generation, collision detection)
- User input handling
- UI text rendering

