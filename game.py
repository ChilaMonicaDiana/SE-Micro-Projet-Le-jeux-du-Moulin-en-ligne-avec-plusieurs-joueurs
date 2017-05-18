"""cogs.py
Includes classes for Intersection, Board, Player"""
from board import Board
from intersection import Intersection
from player import Player


class Game:
    """The complete game with a Board and 2 Players"""
    def __init__(self, playing, observing):
        self.board = Board()
        self.players = (playing, observing, )
        phases = {
            0: "PLACING PIECES",
            1: "MOVING PIECES",
            2: "FLYING",
        }
        self.phase = phases[0]
        outcomes = {
            0: "IN PROGRESS",
            1: "GAME OVER",
        }
        self.outcome = outcomes[0]
        self.turn = False   # Whose turn is it? Either False (0) or True (1)

    def __repr__(self):
        """Print the board"""
        return str(self.board)

    def get_phase(self):
        """Return phase of the game"""
        return self.phase

    def get_turn(self):
        """Return whose turn is it now"""
        return self.turn

    def get_active(self):
        """Get the active player"""
        for player in self.players:
            if player.turn == self.turn:
                return player

    def get_passive(self):
        """Get the passive player"""
        for player in self.players:
            if player.turn != self.turn:
                return player

    def get_board(self):
        """Get the board currently in start_game"""
        return self.board

    def update_state(self):
        """Check and update phase and outcome"""
        phase = self.get_phase()
        print "BEFORE update", phase
        pieces_hand1 = self.get_active().get_pieces_in_hand()
        pieces_hand2 = self.get_passive().get_pieces_in_hand()
        pieces_play1 = self.get_active().get_pieces_in_hand()
        pieces_play2 = self.get_passive().get_pieces_in_hand()
        # Moving Pieces Check
        hand_is_0 = pieces_hand1 == 0 and pieces_hand2 == 0
        enough_pieces = pieces_play1 > 0 and pieces_play2 > 0
        if hand_is_0 and enough_pieces:
            self.phase = "MOVING PIECES"
        # Flying Pieces Check
        few1 = pieces_play1 == 3 and pieces_hand1 == 0
        few2 = pieces_play2 == 3 and pieces_hand2 == 0
        if few1 or few2:
            self.phase = "FLYING"
        # Game Over Check
        too_few1 = pieces_play1 == 2 and pieces_hand1 == 0
        too_few2 = pieces_play2 == 2 and pieces_hand2 == 0
        if too_few1 or too_few2:
            print "GAME HAS ENDED, ACTIVE PLAYER HAS WON"
            self.outcome = "GAME OVER"
            exit(66)
        phase = self.get_phase()
        print "AFTER update", phase

    def check_mills(self, spot):
        """See if a player has created a mill"""
        active = self.get_active()
        turn_number = str(int(active.turn))
        intersection = Intersection(label=spot, owner=None)
        triples = intersection.mills()
        for triple in triples:
            hits = 0
            if spot in triple:
                for letter in triple:
                    if self.board.state[letter] == turn_number:
                        hits += 1
            if hits == 3:
                self.board.is_mill[triple] = True
                print "check_mills() found a mill made for", triple
                return True
        return False

    def put(self, spot):
        """Player puts a Piece on an Intersection"""
        board = self.get_board()
        active = self.get_active()
        passive = self.get_passive()
        active.add_spot(spot)
        board.remove_from_available(spot)
        # Update state for spot in board
        board.state[spot] = str(int(active.turn))
        # Check if phase 1 is reached
        if passive.pieces_in_hand == 0 and active.pieces_in_hand == 0:
            self.phase = "MOVING PIECES"

    def capture(self, spot):
        # Get active and passive
        passive = self.get_passive()
        board = self.get_board()
        intersection = Intersection(label=spot, owner=passive)
        # TODO Checking for a click on a mill leads to a bug
        # triples = intersection.mills()
        # for triple in triples:
        #     assert board.is_mill[triple] is not True
        # TODO move assertion to precondition check before capture
        assert intersection in passive.spots
        passive.remove_spot(spot)
        board.add_to_available(spot)
        board.state[spot] = spot
        # Check if phase 2 is reached:
        if passive.pieces_in_play == 3 and passive.pieces_in_hand == 0:
            self.phase = "FLYING"
        if passive.pieces_in_play == 2 and passive.pieces_in_hand == 0:
            self.outcome = "GAME OVER"

    def move(self, old, new):
        """Move a piece from old spot to new spot"""
        assert self.phase == "MOVING PIECES"
        active = self.get_active()
        turn_num = str(int(active.turn))
        board = self.get_board()
        # Check new spot is a neighbor of old spot
        older = Intersection(label=old, owner=active)
        assert new in older.neighbors()
        assert older
        # Update active player's spots
        active.move_spot(old=old, new=new)
        # Remove active player's piece from old spot
        board.add_to_available(spot=old)
        board.state[old] = old
        # Move active player's piece to new spot
        board.remove_from_available(spot=new)
        board.state[new] = turn_num

    def fly(self, old, new):
        """Move a piece from old spot to new spot"""
        assert self.phase == "FLYING"
        active = self.get_active()
        turn_num = str(int(active.turn))
        board = self.get_board()
        # Update active player's spots
        active.fly_spot(old=old, new=new)
        # Remove active player's piece from old spot
        board.add_to_available(spot=old)
        board.state[old] = old
        # Move active player's piece to new spot
        board.remove_from_available(spot=new)
        board.state[new] = turn_num

    def switch_turn(self):
        """Alternate the turn of the game"""
        self.turn = not bool(self.turn)

    def has_moves(self):
        """Check if passive player has any legal move"""
        passive = self.get_passive()
        # Return True in beginning of game
        if passive.pieces_in_hand > 0:
            return True
        spots = passive.spots_owned()
        board = self.get_board()
        available_spots = board.get_available()
        has_moves = False
        for spot in spots:
            neighbors = spot.neighbors()
            for neighbor in neighbors:
                if neighbor in available_spots:
                    has_moves = True
        return has_moves

    def phase0(self, spot):
        """Placing Pieces"""
        active = self.get_active()
        turn = str(active)
        self.put(spot=spot)
        print self
        # Check if passive player has legal moves
        if not self.has_moves():
            print "Passive player has no legal moves."
            print "^^^^^^ Player" + turn + "has won the game! ^^^^^^"
        mills = self.check_mills(spot)
        if mills:
            print "MILL CREATED"
        # Switch between turn
        self.switch_turn()

    def phase1(self, old, new):
        """Move pieces to neighboring spots only"""
        self.move(old=old, new=new)
        print self
        mills = self.check_mills(new)
        if mills:
            print "MILL CREATED"

    def phase2(self):
        """Fly piece to any available spot"""
        assert self.phase == "FLYING", self.phase
        while self.phase == "FLYING":
            active = self.get_active()
            turn = str(active)
            which = "Player " + turn + ": Which Piece?: "
            old = raw_input(which).upper()
            where = "Player " + str(active) + ": Where To?: "
            new = raw_input(where).upper()
            self.fly(old=old, new=new)
            mills = self.check_mills(new)
            if mills:
                target = raw_input("Target Piece at?: ").upper()
                self.capture(target)
            # Switch between turn
            self.switch_turn()


if __name__ == '__main__':
    p0 = Player(turn=False)
    p1 = Player(turn=True)
    game = Game(playing=p0, observing=p1)
    print "There are 2 players:", game.players
    spot = ''
    old = ''
    new = ''
    game.phase0(spot)
    game.phase1(old, new)
