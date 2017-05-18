import pygame, pygame.font
from player import Player

class Score(pygame.sprite.Sprite):

    def __init__(self, display, score_height, player1, player2):
        turn = {
            True: 2,
            False: 1
        }

        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.PLAYER1_PIECES = player1.pieces_in_hand
        self.PLAYER2_PIECES = player2.pieces_in_hand
        self.PLAYER_TURN = turn[0]

        #Dimensions of the scoreboard
        self.score_h, self.score_w = 50, self.display.get_width()
        self.rect = pygame.Rect(0,0, self.score_w, self.score_h)
        self.bg_color=(160,160,160)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont('American Typewriter', 18, 30)

        self.x_player1_pieces, self.y_player1_pieces = 50.0, 20.0
        self.x_player2_pieces, self.y_player2_pieces = 350.0, 20.0
        self.x_player_turn, self.y_player_turn = 650.0, 20.0

    def print_strings(self):
        self.pieces1_left = "Player 1 Pieces Left: " + str(self.PLAYER1_PIECES)
        self.pieces1_text = self.font.render(self.pieces1_left, True, self.text_color)

        self.pieces2_left = "Player 2 Pieces Left: " + str(self.PLAYER2_PIECES)
        self.pieces2_text = self.font.render(self.pieces2_left, True, self.text_color)

        if self.PLAYER_TURN == 1:
            self.player_turn = "Turn: Player One"
            self.player_text = self.font.render(self.player_turn, True, self.text_color)
        if self.PLAYER_TURN == 2:
            self.player_turn = "Turn: Player One"
            self.player_text = self.font.render(self.player_turn, True, self.text_color)

    def output(self):
        self.print_strings()
        self.display.fill(self.bg_color, self.rect)
        # print scoring strings
        self.display.blit(self.pieces1_text, (self.x_player1_pieces, self.y_player1_pieces))
        self.display.blit(self.pieces2_text, (self.x_player2_pieces, self.y_player2_pieces))
        self.display.blit(self.player_text, (self.x_player_turn, self.y_player_turn))
