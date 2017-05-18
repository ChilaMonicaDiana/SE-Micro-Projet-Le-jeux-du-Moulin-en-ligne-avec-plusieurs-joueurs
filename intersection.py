class Intersection:
    """A representation of each playable spot on the board"""
    def __init__(self, label=' ', owner=None):
        """Assign a LABEL, with owner set to None by default"""
        self.label = label
        self.owner = owner
        # self.mill = False

    def get_label(self):
        """Return label of the spot"""
        return self.label

    def is_empty(self):
        """Check if the spot is empty"""
        return self.owner is None

    def owner(self):
        """Return who occupies the spot"""
        return self.owner    # returns None if there's no owner

    def set_owner(self, player):
        """Set a spot's owner"""
        self.owner = player

    def neighbors(self):
        """List of neighbors for a spot"""
        neighbors = {
            'A': ('B', 'H'),
            'B': ('A', 'C', 'J'),
            'C': ('B', 'D'),
            'D': ('C', 'E', 'L'),
            'E': ('D', 'F'),
            'F': ('E', 'G', 'N'),
            'G': ('F', 'H'),
            'H': ('A', 'G', 'P'),
            'I': ('J', 'P'),
            'J': ('B', 'I', 'K', 'R'),
            'K': ('J', 'L'),
            'L': ('D', 'K', 'M', 'T'),
            'M': ('L', 'N'),
            'N': ('F', 'M', 'O', 'V'),
            'O': ('N', 'P'),
            'P': ('H', 'I', 'O', 'X'),
            'Q': ('R', 'X'),
            'R': ('J', 'Q', 'S'),
            'S': ('R', 'T'),
            'T': ('L', 'S', 'U'),
            'U': ('T', 'V'),
            'V': ('N', 'U', 'W'),
            'W': ('V', 'X'),
            'X': ('P', 'Q', 'W'),
        }
        return neighbors[self.label]

    def mills(self):
        """List of neighbors for a spot"""
        mills = {
            'A': ('ABC', 'AGH'),
            'B': ('ABC', 'BJR'),
            'C': ('ABC', 'CDE'),
            'D': ('CDE', 'DLT'),
            'E': ('CDE', 'EFG'),
            'F': ('EFG', 'FNV'),
            'G': ('AGH', 'EFG'),
            'H': ('AGH', 'HPX'),
            'I': ('IJK', 'IOP'),
            'J': ('BJR', 'IJK'),
            'K': ('IJK', 'KLM'),
            'L': ('DLT', 'KLM'),
            'M': ('KLM', 'MNO'),
            'N': ('FNV', 'MNO'),
            'O': ('IOP', 'MNO'),
            'P': ('HPX', 'IOP'),
            'Q': ('QRS', 'QWX'),
            'R': ('BJR', 'QRS'),
            'S': ('QRS', 'STU'),
            'T': ('DLT', 'STU'),
            'U': ('STU', 'UVW'),
            'V': ('FNV', 'UVW'),
            'W': ('QWX', 'UVW'),
            'X': ('HPX', 'QWX'),
        }
        return mills[self.label]

    def __repr__(self):
        """Representation of the spot"""
        return str(self.label)

    def __eq__(self, label):
        """Check if the label of the spot matches other"""
        return self.label == label
