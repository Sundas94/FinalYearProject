import random
import sys
import pyglet

# Defining colours and shapes


colours = [
(128, 128, 128), # grey
(0, 255, 255), # cyan 
(0, 0, 255), # blue
(124, 252, 0), # green
(255, 165, 0), # orange
(138, 43, 226), #purple
(255, 0 , 0) # red
(255, 255, 0) # yellow
]

# Define the shapes 
  _shapes = [
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]],
        
        [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
        
        [[0, 0, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 1, 1, 0]],
        
        [[0, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 1, 0]],
        
        [[0, 0, 0, 0], 
         [0, 0, 1, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0]],
        
        [[0, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 1, 0]],

        [[0, 0, 0, 0],
         [0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0]]
    ]