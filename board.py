from intersection import Intersection


class Board:
    def __init__(self):
        import string
        letters = list(filter(lambda x: x < "Y", string.ascii_uppercase))
        available = list()
        state = dict()

        for letter in letters:
            intersection = Intersection(label=letter, owner=None)
            available.append(intersection)
            state[letter] = ''
        self.state = state
        self.available = available

        triples = (
            'ABC', 'AGH', 'BJR', 'CDE', 'DLT', 'EFG', 'FNV', 'HPX',
            'IJK', 'IOP', 'KLM', 'MNO', 'QRS', 'QWX', 'STU', 'UVW',
        )
        self.is_mill = dict.fromkeys(triples, False)

    def add_to_available(self, spot):
        intersection = Intersection(label=spot)
        self.available.append(intersection)
        self.available = sorted(self.available)

    def remove_from_available(self, spot):
        intersection = Intersection(label=spot)
        self.available.remove(intersection)

    def get_available(self):
        """Return list of available spots"""
        return self.available

    def __str__(self):
        pretty = [
            ['A', ' ', ' ', 'B', ' ', ' ', 'C'],
            [' ', 'I', ' ', 'J', ' ', 'K', ' '],
            [' ', ' ', 'Q', 'R', 'S', ' ', ' '],
            ['H', 'P', 'X', ' ', 'T', 'L', 'D'],
            [' ', ' ', 'W', 'V', 'U', ' ', ' '],
            [' ', 'O', ' ', 'N', ' ', 'M', ' '],
            ['G', ' ', ' ', 'F', ' ', ' ', 'E'],
        ]
        for row in pretty:
            for i, char in enumerate(row):
                if char.isalpha() and char not in self.available:
                    row[i] = self.state[char]
        return str('\n'.join([''.join(['{:3}'.format(item) for item in row])
                              for row in pretty]))
