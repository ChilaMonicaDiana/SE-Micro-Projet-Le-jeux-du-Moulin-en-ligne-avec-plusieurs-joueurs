import pygame
import os
import sys
#from Piece import Piece
from Score import Score
from game import Game
from player import Player
from intersection import Intersection
from board import Board
import pygame.gfxdraw
from piece import Piece

#GLOBAL VARIABLES

WINDOW_SIZE = (1000, 650)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIECES = [0]* 18
BOARD = [0] * 24

def play_game():
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont('Verdana', 25)
    pygame.display.set_caption("Nine Men's Morris!")
    DISPLAY_SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    DISPLAY_SCREEN.fill(GREY)
    DISPLAY_SCREEN.blit(pygame.image.load('board.bmp'), (20, 60))
    clock = pygame.time.Clock()
    PLAYER1_IMG = pygame.image.load('white.png')
    PLAYER2_IMG = pygame.image.load('black.png')
    START_RECT = PLAYER1_IMG.get_rect()
    START_RECT2 = PLAYER2_IMG.get_rect()
    IMAGE_RECT = START_RECT
    IMAGE2_RECT = START_RECT2
    pos = pygame.mouse.get_pos()
    DONE = False
    TURN = 1
    SCORE_HEIGHT = 50

    playing = Player(True)
    observing = Player(False)
    score = Score(DISPLAY_SCREEN, SCORE_HEIGHT, playing, observing)

    mylist = list()
    charsList = list()

    game = Game(playing, observing)

    all_sprites_list = pygame.sprite.Group()
    while not DONE:
        for i, a in intersections:
            mylist = a
            charsList = i
            pygame.gfxdraw.box(DISPLAY_SCREEN, a, (255,255,255,0.5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.phase == "PLACING PIECES":
                    mouse_pos = list(event.pos)
                    #print mouse_pos
                    IMAGE_RECT = START_RECT.move(mouse_pos)
                    IMAGE2_RECT = START_RECT2.move(mouse_pos)
                    #Game Phase 0
                    if score.PLAYER_TURN == 1 and score.PLAYER1_PIECES != 0:
                        for i, a in intersections:
                            if not IMAGE_RECT.colliderect(a):
                                pass
                            else:
                                print i
                                DISPLAY_SCREEN.blit(PLAYER1_IMG, a)
                                score.PLAYER1_PIECES -= 1
                                game.put(spot=i)
                                piece = Piece(label=i)
                                all_sprites_list.add(piece)
                                print all_sprites_list.sprites()
                                #print all_sprites_list()
                                mills = game.check_mills(i)
                                # if not game.has_moves():
                                #     print "Passive player has no legal moves."
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        for i, a in intersections:
                                            if mouse_pos.colliderect(a):
                                                print "mouse collided with spot"
                                                game.capture(i)
                                                for element in all_sprites_list:
                                                    if element.label == i:
                                                        print "found piece"

                    if score.PLAYER_TURN == 2 and score.PLAYER2_PIECES != 0:
                        for i, a in intersections:
                            if not IMAGE_RECT.colliderect(a):
                                pass
                            else:
                                DISPLAY_SCREEN.blit(PLAYER2_IMG, a)
                                score.PLAYER2_PIECES -= 1
                                game.put(spot=i)
                                piece = Piece(label=i)
                                all_sprites_list.add(piece)
                                print all_sprites_list.sprites()
                                #print all_sprites_list()[-1]
                                mills = game.check_mills(i)
                                # if not game.has_moves():
                                #     print "Passive player has no legal moves."

                                print "capturing a piece"
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        for i, a in intersections:
                                            if IMAGE_RECT.colliderect(a):
                                                game.capture(i)
                                                for piece in all_sprites_list:
                                                    print piece.label
                                                    if piece.label == i:
                                                        print "found piece"
                                print "captured a piece"


                                # Switch between turn
                                #game.switch_turn()
                score.PLAYER_TURN = score.PLAYER_TURN % 2 + 1
            #phase1
            score.output()
        pygame.display.update()
        clock.tick(60)

mills = []

# pixel coordinates of nodes on board
intersections = [

                ('A', ((20, 60, 40, 40))),
                ('B', ((273, 60, 40, 40))),
                ('C', ((527, 60, 40, 40))),
                ('D', ((527, 316, 40, 40))),
                ('E', ((527, 568, 40, 40))),
                ('F', ((273, 568, 40, 40))),
                ('G', ((20, 568, 40, 40))),
                ('H', ((20, 316, 40, 40))),

                ('I', ((101, 140, 40, 40))),
                ('J', ((272, 140, 40, 40))),
                ('K', ((442, 140, 40, 40))),
                ('L', ((442, 316, 40, 40))),
                ('M', ((442, 480, 40, 40))),
                ('N', ((272, 480, 40, 40))),
                ('O', ((101, 480, 40, 40))),
                ('P', ((101, 316, 40, 40))),

                ('Q', ((186, 227, 40, 40))),
                ('R', ((274, 227, 40, 40))),
                ('S', ((361, 227, 40, 40))),
                ('T', ((361, 317, 40, 40))),
                ('U', ((361, 398, 40, 40))),
                ('V', ((274, 398, 40, 40))),
                ('W', ((186, 398, 40, 40))),
                ('X', ((186, 317, 40, 40)))]


# class Intro_Screen():
#     def __init__(self, display, objects, BACKGROUND_C=(160,160,160), font='None', font_size=40,
#                     font_color=(0, 25, 51)):
#         self.display = display
#         self.display_width = self.display.get_rect().width
#         self.display_height = self.display.get_rect().height
#
#         self.BACKGROUND_C = BACKGROUND_C
#         self.clock = pygame.time.Clock()
#
#         self.objects = objects
#         #initialize the font
#         pygame.font.init()
#         self.font = pygame.font.SysFont('Courier', font_size, 1, 1)
#         self.font_color = font_color
#
#         self.objects = []
#
#         for i, item in enumerate(objects):
#             label = self.font.render(item, 1, font_color)
#
#             width = label.get_rect().width
#             height = label.get_rect().height
#
#             x_pos = (self.display_width / 2) - (width / 2)
#             height_block = len(objects) * height
#             y_pos = (self.display_height / 2) - (height_block / 2) + (i * height)
#
#             self.objects.append([item, label, (width, height), (x_pos, y_pos)])
#
#     def run(self):
#         mainloop = True
#         pygame.font.init()
#         while mainloop:
#             # Limit frame speed to 50 FPS
#             self.clock.tick(50)
#
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     mainloop = False
#
#             pressed = pygame.key.get_pressed()
#             if pressed[pygame.K_2]:
#                 play_game()
#             if pressed[pygame.K_q]:
#                 sys.exit()
#
#             # Redraw the background
#             self.display.fill(self.BACKGROUND_C)
#
#             for name, label, (width, height), (x_pos, y_pos) in self.objects:
#                 self.display.blit(label, (x_pos, y_pos))
#
#             pygame.draw.rect(DISPLAY_SCREEN, BLACK,(150,450,100,50))
#             pygame.font.Font.render("TESTING", True,  WHITE, (150,450))
#             pygame.draw.rect(DISPLAY_SCREEN, BLACK,(550,450,100,50))
#
#             pygame.display.flip()

if __name__ == '__main__':
    # DISPLAY_SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    # menu_items = ('Play Nine Mens Morris!', 'Choose # of Players', 'Choose 1 or 2 to see who goes first!')
    #
    # pygame.display.set_caption("NINE MEN'S MORRIS")
    # game_Loop = Intro_Screen(DISPLAY_SCREEN, menu_items)
    # game_Loop.run()
    play_game()
