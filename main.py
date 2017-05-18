import pygame
# import os
import sys
from Score import Score
from game import Game
from player import Player

# GLOBAL VARIABLES
WINDOW_SIZE = (1000, 650)
GREY = (160, 160, 160)
YELLOW = (255, 253, 203)
WHITE = (0, 255, 255)
BLACK = (0, 0, 0)
PIECES = [0] * 18
BOARD = [0] * 24
background = pygame.image.load('board.bmp')


def play_game():
    pygame.init()
    pygame.font.init()
    # font = pygame.font.SysFont('Verdana', 25)
    pygame.display.set_caption("Nine Men's Morris!")
    display_screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    display_screen.fill(YELLOW)
    display_screen.blit(background, (20, 60))
    player1_piece = pygame.image.load('white.png')
    player2_piece = pygame.image.load('black.png')
    # START_RECT = player1_piece.get_rect()
    # START_RECT2 = player2_piece.get_rect()
    # IMAGE_RECT = START_RECT
    # IMAGE2_RECT = START_RECT2
    done = False
    turn = 1
    score_height = 50
    pos = pygame.mouse.get_pos()
    clock = pygame.time.Clock()
    clicked = False

    playing = Player(True)
    observing = Player(False)
    score = Score(display_screen, score_height, playing, observing)

    mylist = list()
    charsList = list()

    game = Game(playing, observing)

    # print "hello"
    while not done:
        for letter, a in intersections:
            rect = pygame.Rect(a)
            # charsList = letter
            # pygame.draw.rect(display_screen, WHITE, a)
            display_screen.blit(player1_piece, rect)
            # Get mouse position
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(pos):
                    print "MOUSE clicked!"
                    clicked = not clicked
                display_screen.blit(player1_piece, rect)
                if clicked:
                    display_screen.blit(background, (17, 63), rect)

                    # score.PLAYER_TURN = score.PLAYER_TURN % 2 + 1
            # phase1
            score.output()
        pygame.display.update()
        clock.tick(60)

# pixel coordinates of nodes on board
intersections = [
    ('A', (17, 63, 54, 52), ),
    ('B', (270, 63, 54, 52), ),
    ('C', (525, 63, 54, 52), ),
    ('D', (525, 316, 54, 52), ),
    ('E', (525, 568, 54, 52), ),
    ('F', (270, 568, 54, 52), ),
    ('G', (17, 568, 54, 52), ),
    ('H', (17, 316, 54, 52), ),
    ('I', (102, 145, 54, 52), ),
    ('J', (270, 145, 54, 52), ),
    ('K', (438, 145, 54, 52), ),
    ('L', (438, 316, 54, 52), ),
    ('M', (438, 486, 54, 52), ),
    ('N', (270, 486, 54, 52), ),
    ('O', (102, 486, 54, 52), ),
    ('P', (102, 316, 54, 52), ),
    ('Q', (187, 225, 54, 52), ),
    ('R', (270, 225, 54, 52), ),
    ('S', (353, 225, 54, 52), ),
    ('T', (353, 316, 54, 52), ),
    ('U', (353, 396, 54, 52), ),
    ('V', (270, 396, 54, 52), ),
    ('W', (187, 396, 54, 52), ),
    ('X', (187, 316, 54, 52), ),
]


if __name__ == '__main__':
    play_game()
