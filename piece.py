"""piece.py

Contains the Piece class to represent the gamepiece on a NineMensMorris board"""
import pygame


class Piece(pygame.sprite.Sprite):
    """A Piece with a given color, coordinates and image"""
    def __init__(self, label, turn):
        """Set label, color, coordinates, and image to a Piece"""
        super(Piece, self).__init__()
        color = {False: 'white', True: 'black'}
        self.label = label
        self.color = color[turn]
        length = 54
        width = 52
        spots = {
            'A': (17, 63, length, width),
            'B': (270, 63, length, width),
            'C': (525, 63, length, width),
            'D': (525, 316, length, width),
            'E': (525, 568, length, width),
            'F': (270, 568, length, width),
            'G': (17, 568, length, width),
            'H': (17, 316, length, width),
            'I': (102, 145, length, width),
            'J': (270, 145, length, width),
            'K': (438, 145, length, width),
            'L': (438, 316, length, width),
            'M': (438, 486, length, width),
            'N': (270, 486, length, width),
            'O': (102, 486, length, width),
            'P': (102, 316, length, width),
            'Q': (187, 225, length, width),
            'R': (270, 225, length, width),
            'S': (353, 225, length, width),
            'T': (353, 316, length, width),
            'U': (353, 396, length, width),
            'V': (270, 396, length, width),
            'W': (187, 396, length, width),
            'X': (187, 316, length, width),
        }
        self.coordinates = spots[label]
        self.rect = pygame.Rect(self.coordinates)
        filename = "%s.png" % color[turn]
        self.image = pygame.image.load(filename)

    def __eq__(self, label):
        """Check a Piece against a label"""
        return self.label == label

    def __str__(self):
        """String print"""
        return str(self.label)

    def __repr__(self):
        """String representation"""
        return str(self.label)

    def get_rect(self):
        """Return pygame Rect of coordinates"""
        rect = pygame.Rect(self.coordinates)
        return rect
