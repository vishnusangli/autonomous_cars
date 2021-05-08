# Self Driving Car Object through training an Autonomous RL Car Agent
This project involves developing an deep learning driving and drifting automobile, represented as a simplistic rectangular obj in a wireframe world
## Track Environment
wall-define Track equations comprised of 
- Straight Line Elements
- Trun Elements characterised as Circular Arcs
- First StartingStrip is a subclass of the Line Element, involving a back wall to restrict out-of-track

## Math Backend
- Equation class 
- Function Solver
- Grid-based wrapper for the function solver, aiding us to track and and find intersections from a group of equations

## Basic Car Sprite
A rectangular car sprite controlled by WASD input. 
- Steering and regular turn imementations
- Drifting branch contains a rudimentary form of drifting (Works only with steering turn)

## Deep Q-Learning Model
- Implemented in tensorflow v1
- Reward system involving major penalty for collision along with a linear reward function from car's instantaneous speed
- Epsiodes allowing a single collision or 10 seconds at 20 fps
- Input state is a (1, 1, 9) array with:
  - 8 lines of sight equally distributed from [0 - 2pi], given as a fraction of max line of sight
  - Instantaneous speed scaled between [min_speed, max_speed] as [0, 1]

Current final trial7 NN model: 
- Dense(9) input layer
- Flatten layer 
- Dense layer with linear activation
- Dense(8) output layer
Model prioritises remaining still over moving although it actively recieves penalty as insufficient training/insufficient braking decelration makes collision guaranteed when moving, thereby receiving greater penatly than a static episode.
Potential Fixes: 
- Increase turn rate, reduce acceleration.
- Reduce penalty for crashing and implement a shifted inverse speed-reward relationship that would provide higher penalty for remaining still.


