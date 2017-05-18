"""scoreboard.py

Contains the Scoreboard class to display number of pieces left
and whose turn is it"""
import pygame


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, display, game):
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        # Dimensions of the scoreboard
        self.score_h, self.score_w = 50, self.display.get_width()
        self.rect = pygame.Rect(0, 0, self.score_w, self.score_h)
        self.bg_color = (255, 253, 203)     # Yellow
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('American Typewriter', 18, 30)

        # Position coordinates
        self.p1_x, self.p1_y = 50.0, 20.0
        self.p2_x, self.p2_y = 350.0, 20.0
        self.turn_x, self.turn_y = 650.0, 20.0
        self.phase_x, self.phase_y = 650.0, 200.0
        # Game properties
        self.game = game
        self.active = game.get_active()
        self.passive = game.get_passive()
        self.turn = game.get_turn()
        self.phase = game.get_phase()
        self.phase_text = self.font.render(self.phase, True, self.text_color)

    def print_strings(self):
        hand = self.active.get_pieces_in_hand()
        play = self.active.get_pieces_in_play()
        header = ''
        if self.phase == "PLACING PIECES":
            header = "White Pieces Left: %i" % hand
        elif self.phase == "MOVING PIECES":
            header = "Black Pieces in Play: %i" % play
            self.phase_text = "MOVING PIECES"
        self.pieces1_text = self.font.render(header, True, self.text_color)

        hand = self.passive.get_pieces_in_hand()
        play = self.passive.get_pieces_in_play()
        if self.phase == "PLACING PIECES":
            header = "Black Pieces Left: %i" % hand
        elif self.phase == "MOVING PIECES":
            header = "Black Pieces in Play: %i" % play
        self.pieces2_text = self.font.render(header, True, self.text_color)

        turn = ''
        if self.turn is False:
            turn = "Turn: White"
        if self.turn is True:
            turn = "Turn: Black"
        self.player_text = self.font.render(turn, True, self.text_color)

        # self.phase_text = self.font.render(self.phase, True, self.text_color)

    def output(self, phase_text):
        self.print_strings()
        self.display.fill(self.bg_color, self.rect)

        self.phase = self.game.get_phase()
        self.phase_text = self.font.render(self.phase, True, self.text_color)
        # self.phase_text = self.font.render(phase_text, True, self.text_color)
        # print scoring strings
        self.display.blit(self.pieces1_text, (self.p1_x, self.p1_y))
        self.display.blit(self.pieces2_text, (self.p2_x, self.p2_y))
        self.display.blit(self.player_text, (self.turn_x, self.turn_y))
        self.display.blit(self.phase_text, (self.phase_x, self.phase_y))
        # print "scoreboard phase_text", self.phase

    def switch_turn(self):
        self.turn = not bool(self.turn)