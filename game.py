from itertools import cycle
class Game:
    def __init__(self):
        self._data = {}
        self._turns = cycle([1,-1])
        self._player = next(self._turns)

    def move(self, pos):
        if self._data.get(pos): return
        self._data[pos] = self._player
        self._player = next(self._turns)

    @property
    def data(self):
        return self._data.items()