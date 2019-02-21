# Pursuer-Evader-ROS
Implementation of Evader robot avoiding obstacles and a pursuer following it in ROS 

EVADER

This project contains a controller node that drives the robot straight at a constant speed of 2m/s. When the robot is close to an obstacle, the robot stops, turns in a random new direction,and drives at the same speed. The robot has a laser range finder attached to it and the output of the sensor from the stage world file is read and observed to avoid the obstacles.

PURSUER

The coordinate frame of the evader robot wrt the global frame are published. A new world file is created with a second robot called pursuer, and dropped into the world close to the evader robot. Another controller node is written for the pursuer that subscribes to the tf messages from the evader, and follows the evader by going to the spot it was at from one second before.

