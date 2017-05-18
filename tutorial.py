import pygame
import os
from game import Game
from piece import Piece
from player import Player
from scoreboard import Scoreboard


# Helper functions
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def get_mouse_rect():
    """Get mouse location rectangle in pygame Rect format"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Make a square rectangle with the x, y coordinates
    mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
    return mouse_rect


class NineMensMorris:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Nine Men's Morris!")
        self.spots = {
            'A': (17, 63, 54, 52),
            'B': (270, 63, 54, 52),
            'C': (525, 63, 54, 52),
            'D': (525, 316, 54, 52),
            'E': (525, 568, 54, 52),
            'F': (270, 568, 54, 52),
            'G': (17, 568, 54, 52),
            'H': (17, 316, 54, 52),
            'I': (102, 145, 54, 52),
            'J': (270, 145, 54, 52),
            'K': (438, 145, 54, 52),
            'L': (438, 316, 54, 52),
            'M': (438, 486, 54, 52),
            'N': (270, 486, 54, 52),
            'O': (102, 486, 54, 52),
            'P': (102, 316, 54, 52),
            'Q': (187, 225, 54, 52),
            'R': (270, 225, 54, 52),
            'S': (353, 225, 54, 52),
            'T': (353, 316, 54, 52),
            'U': (353, 396, 54, 52),
            'V': (270, 396, 54, 52),
            'W': (187, 396, 54, 52),
            'X': (187, 316, 54, 52),
        }
        # Setup backend
        playing = Player(True)
        observing = Player(False)
        self.game = Game(playing, observing)
        # Setup cogs
        self.playing = self.game.get_active()
        self.observing = self.game.get_passive()
        self.board = self.game.get_board()
        self.all_sprites_list = pygame.sprite.Group()
        self.background = pygame.image.load('background.png')
        self.turn = self.game.turn
        # Setup screen
        resolution = (1000, 650)
        self.screen = pygame.display.set_mode(resolution)
        self.screen_init()
        # Setup scoreboard
        self.score = Scoreboard(self.screen, self.game)
        self.done = False
        # self.clicked = False
        self.phase = self.game.get_phase()
        self.clock = pygame.time.Clock()

    def screen_init(self):
        # Screen setup
        yellow = (255, 253, 203)
        self.screen.fill(yellow)
        self.screen.blit(self.background, (0, 0))

    def update(self):
        self.all_sprites_list.update()
        self.screen_init()
        self.all_sprites_list.draw(self.screen)
        self.score.output(self.phase)
        pygame.display.update()

    def switch_turn(self):
        self.game.switch_turn()
        self.score.switch_turn()

    def get_phase(self):
        return self.game.get_phase()

    def clicked_available(self):
        for event in pygame.event.get():
            # Exit by clicking on close window
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_rect = get_mouse_rect()
                for intersection in self.board.get_available():
                    label = intersection.get_label()
                    spot_rect = pygame.Rect(self.spots[label])
                    if spot_rect.colliderect(mouse_rect):
                        return label
        return ''

    def clicked_active(self):
        for event in pygame.event.get():
            # Exit by clicking on close window
            if event.type == pygame.QUIT:
                self.done = True
                exit(2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_rect = get_mouse_rect()
                spots_owned = self.game.get_active().spots_owned()
                for intersection in spots_owned:
                    label = intersection.get_label()
                    spot_rect = pygame.Rect(self.spots[label])
                    if spot_rect.colliderect(mouse_rect):
                        return label
        return ''

    def clicked_passive(self):
        for event in pygame.event.get():
            # Exit by clicking on close window
            esc = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            clicked_x = event.type == pygame.QUIT
            if clicked_x or esc:
                self.done = True
                exit(2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_rect = get_mouse_rect()
                spots_owned = self.game.get_passive().spots_owned()
                for intersection in spots_owned:
                    label = intersection.get_label()
                    spot_rect = pygame.Rect(self.spots[label])
                    if spot_rect.colliderect(mouse_rect):
                        return label
        return ''

    def phase0(self):
        """Play in phase0"""
        self.game.update_state()
        if self.game.phase == 'MOVING PIECES':
            self.update()
            self.phase1()
        clicked_spot = self.clicked_available()
        self.score.output(self.phase)
        if clicked_spot.isalpha():
            self.game.put(spot=clicked_spot)

            # TODO move the lines below to a different function
            piece = Piece(label=clicked_spot, turn=self.game.turn)
            x, y, l, w = piece.coordinates
            self.screen.blit(piece.image, (x, y))
            self.all_sprites_list.add(piece)
            self.all_sprites_list.draw(self.screen)
            pygame.display.update()

            if not self.game.has_moves():
                print "Passive player has no legal moves."
                print "^^^^^^ Active Player has won the game! ^^^^^^"
                self.done = True
                exit(7)

            mills = self.game.check_mills(clicked_spot)
            if mills:
                print "MILL CREATED IN phase0"
                target = self.clicked_passive()
                while target == '':
                    target = self.clicked_passive()
                if target != '':
                    for element in self.all_sprites_list.sprites():
                        if element == target:
                            self.all_sprites_list.remove(element)
                            assert element not in self.all_sprites_list.sprites()
                            self.game.capture(element.label)
                            self.update()

                            pygame.display.update()
            self.score.output(self.phase)
            self.switch_turn()
        self.game.update_state()

    def phase1(self):
        """Play in phase1"""
        if self.game.phase == 'FLYING':
            self.update()
            self.phase2()
        if self.game.get_phase() != "MOVING PIECES":
            return
        self.game.update_state()
        # phase = self.get_phase()
        # assert self.phase == "MOVING PIECES", "self.phase: %s" % phase
        print "PHASE1 DEFINITELY RUNNING"
        target = self.clicked_active()
        while target == '':
            target = self.clicked_active()
        print "Printing target", target
        dest = self.clicked_available()
        while dest == '':
            dest = self.clicked_available()
        print "Printing dest", dest
        print self.phase, "here"
        self.score.output(self.phase)
        if target.isalpha() and dest.isalpha():
            # print clicked_spot

            if target != '' and dest != '':
                for element in self.all_sprites_list.sprites():
                    if element == target:
                        # Removing a Piece from target location
                        self.all_sprites_list.remove(element)
                        assert element not in self.all_sprites_list.sprites()
                        # print "PRINTING SPRITE LIST:", self.all_sprites_list.sprites()
                        self.update()
                        pygame.display.update()
                        assert element not in self.all_sprites_list.sprites()
                        self.game.move(old=target, new=dest)

                        # Adding a Piece to destination
                        piece = Piece(label=dest, turn=self.game.turn)
                        x, y, l, w = piece.coordinates
                        self.screen.blit(piece.image, (x, y))
                        self.all_sprites_list.add(piece)
                        self.all_sprites_list.update()
                        # self.screen_init()
                        self.all_sprites_list.draw(self.screen)
                        pygame.display.update()
                        morris.clock.tick(60)

            if self.game.get_active().pieces_in_hand == 0 and \
                    self.game.get_passive().pieces_in_hand == 0:
                self.phase = "MOVING PIECES"

            if not self.game.has_moves():
                print "Passive player has no legal moves."
                print "^^^^^^ Active Player has won the game! ^^^^^^"
                self.done = True
                exit(666)

            mills = self.game.check_mills(dest)
            if mills:
                print "MILL CREATED IN phase1 BUGGY scoreboard"
                self.score.output(self.phase)
                target = self.clicked_passive()
                while target == '':
                    target = self.clicked_passive()
                if target != '':
                    # print "Target is ", target
                    for element in self.all_sprites_list.sprites():
                        if element == target:
                            # print "Found piece to remove"
                            self.all_sprites_list.remove(element)
                            assert element not in self.all_sprites_list.sprites()
                            self.game.capture(element.label)
                            self.update()
                            pygame.display.update()
                            morris.clock.tick(60)
            self.score.output(self.phase)
            self.switch_turn()
        self.game.update_state()

    def phase2(self):
        """Play in phase2"""
        self.game.update_state()
        # phase = self.get_phase()
        # assert self.phase == "MOVING PIECES", "self.phase: %s" % phase
        print "PHASE2 DEFINITELY RUNNING"
        target = self.clicked_active()
        while target == '':
            target = self.clicked_active()
        print "Printing target", target
        dest = self.clicked_available()
        while dest == '':
            dest = self.clicked_available()
        print "Printing dest", dest
        print self.phase
        self.score.output(self.phase)
        if target.isalpha() and dest.isalpha():
            # print clicked_spot

            if target != '' and dest != '':
                for element in self.all_sprites_list.sprites():
                    if element == target:
                        # Removing a Piece from target location
                        self.all_sprites_list.remove(element)
                        assert element not in self.all_sprites_list.sprites()
                        # print "PRINTING SPRITE LIST:", self.all_sprites_list.sprites()
                        self.update()
                        pygame.display.update()
                        assert element not in self.all_sprites_list.sprites()
                        self.game.fly(old=target, new=dest)

                        # Adding a Piece to destination
                        piece = Piece(label=dest, turn=self.game.turn)
                        x, y, l, w = piece.coordinates
                        self.screen.blit(piece.image, (x, y))
                        self.all_sprites_list.add(piece)
                        self.all_sprites_list.update()
                        # self.screen_init()
                        self.all_sprites_list.draw(self.screen)
                        pygame.display.update()
                        morris.clock.tick(60)

            # if self.game.get_active().pieces_in_hand == 0 and \
            #         self.game.get_passive().pieces_in_hand == 0:
            #     self.phase = "MOVING PIECES"

            if not self.game.has_moves():
                print "Passive player has no legal moves."
                print "^^^^^^ Active Player has won the game! ^^^^^^"
                self.done = True
                exit(666)

            mills = self.game.check_mills(dest)
            if mills:
                print "MILL CREATED IN phase1 BUGGY scoreboard"
                self.score.output(self.phase)
                target = self.clicked_passive()
                while target == '':
                    target = self.clicked_passive()
                if target != '':
                    # print "Target is ", target
                    for element in self.all_sprites_list.sprites():
                        if element == target:
                            # print "Found piece to remove"
                            self.all_sprites_list.remove(element)
                            assert element not in self.all_sprites_list.sprites()
                            self.game.capture(element.label)
                            self.update()
                            pygame.display.update()
                            morris.clock.tick(60)
            self.score.output(self.phase)
            self.switch_turn()
        self.game.update_state()


if __name__ == '__main__':
    morris = NineMensMorris()
    while not morris.done:
        # print morris.phase
        if morris.phase == 'PLACING PIECES':
            morris.score.output(morris.phase)
            pygame.display.update()
            morris.phase0()
        # pygame.display.update()
        if morris.phase == 'MOVING PIECES':
            morris.score.output(morris.phase)
            pygame.display.update()
            morris.phase1()
        if morris.phase == 'FLYING':
            morris.score.output(morris.phase)
            pygame.display.update()
            morris.phase2()
        morris.clock.tick(60)
