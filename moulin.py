#!/usr/bin/env python
# Modified code from: https://github.com/asrivat1/DeepLearningVideoGames and http://programarcadegames.com/index.php?chapter=introduction_to_graphics
# which is in turn Modified from http://www.pygame.org/project-Very+simple+Pong+game-816-.html

import numpy as np
import pygame
from threading import Thread
from threading import Event
from time import sleep
import ai

# SETTINGS
GUI = False
BACKGROUND = (90, 90, 90) # gray
PLAYER1 = (240, 240, 240) # almost white
PLAYER2 = (10, 10, 10) # almost black
LINES = (255, 255, 255) # white

TAKE_PIECE_REWARD = 0.2
WIN_REWARD = 1

# globals - don't change
clickCondition = Event()
clickX = 0
clickY = 0

# pygame input
def blockGetClickIndex():
    global clickX, clickY, clickCondition
    # wait for click event and copy coordinates
    while clickX == clickY == 0:
        try:
            clickCondition.wait(1)
        except KeyboardInterrupt:
            return -1
    x = clickX
    y = clickY
    clickX = clickY = 0
    clickCondition.clear()
    
    # look up piece
    for i in range(24):
        dx = x - 50*getCoords(i)[0]
        dy = y - 50*getCoords(i)[1]
        if dx**2 + dy**2 <= 30**2: # x^2 + y^2 <= r^2
            return i
    
    return -1

# Lookup table for what fields are above others, nicer and more readable than if's
above_arr = [-1, -1, -1,    -1, 1, -1,    -1, 4, -1,    0, 3, 6,    8, 5, 2,    11, -1, 12,    10, 16, 13,    9, 19, 14]
# Lookup table for coordinates
coord_arr = np.array([(1,1), (7,1), (13,1),    (3,3), (7,3), (11,3),    (5,5), (7,5), (9,5),    (1,7), (3,7), (5,7),
                    (9,7), (11,7), (13,7),    (5,9), (7,9), (9,9),    (3,11), (7,11), (11,11),    (1,13), (7,13), (13,13)], dtype=[('x', 'i4'),('y', 'i4')])

def indexAbove(i):
    return above_arr[i]
def indexBelow(i):
    try:
        return above_arr.index(i)
    except ValueError:
        return -1
def indexLeft(i):
    if i % 3 == 0:
        return -1
    else:
        return i-1
def indexRight(i):
    if i % 3 == 2:
        return -1
    else:
        return i+1
def getCoords(i):
    return [coord_arr['x'][i], coord_arr['y'][i]]
