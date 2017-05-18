from intersection import Intersection


class Player:
    """Either a Human or AI who's participating in the game"""
    def __init__(self, turn):
        self.turn = turn        # Either True or False
        self.pieces_in_hand = 9    # number of available pieces
        self.pieces_in_play = 0
        self.spots = list()      # spots held by the player

    def __eq__(self, turn):
        return self.turn == turn

    def get_pieces_in_hand(self):
        return self.pieces_in_hand

    def get_pieces_in_play(self):
        return self.pieces_in_play

    def spots_owned(self):
        return self.spots

    def add_spot(self, spot):
        intersection = Intersection(label=spot, owner=self)
        self.spots.append(intersection)
        self.pieces_in_hand -= 1
        self.pieces_in_play += 1

    def remove_spot(self, spot):
        intersection = Intersection(label=spot, owner=None)
        self.spots.remove(intersection)
        self.pieces_in_play -= 1

    def move_spot(self, old, new):
        older = Intersection(label=old, owner=self)
        newer = Intersection(label=new, owner=self)
        self.spots.remove(older)
        self.spots.append(newer)

    def fly_spot(self, old, new):
        self.move_spot(old, new)

    def __repr__(self):
        return str(int(self.turn))
