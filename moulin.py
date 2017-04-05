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
