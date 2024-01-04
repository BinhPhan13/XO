from itertools import cycle
class Game:
    def __init__(self):
        self._data = {}
        self._turns = cycle([1,-1])
        self._player = next(self._turns)

        self._last_pos = None
        self.streak = tuple()

    def undo(self):
        if len(self._data) <= 1: return
        self._data.pop(self._last_pos)
        self._player = next(self._turns)

        marks = list(self._data)
        self._last_pos = marks[-1]
        self.streak = tuple()

    def move(self, pos):
        if pos in self._data: return
        if self.streak: return

        self._data[pos] = self._player
        self._player = next(self._turns)

        self._last_pos = pos
        self.streak = self._check_win()

    def _check_win(self):
        row, col = self._last_pos
        player = self._data[row,col]

        # row
        sc, ec = col, col
        while self._data.get((row,sc)) == player: sc -= 1
        while self._data.get((row,ec)) == player: ec += 1

        streak = tuple((row,c) for c in range(sc+1, ec))
        if len(streak) >= 5: return streak

        # col
        sr, er = row, row
        while self._data.get((sr,col)) == player: sr -= 1
        while self._data.get((er,col)) == player: er += 1

        streak = tuple((r,col) for r in range(sr+1, er))
        if len(streak) >= 5: return streak

        # \
        sr, er, sc, ec = row, row, col, col
        while self._data.get((sr,sc)) == player: sr, sc = sr-1, sc-1
        while self._data.get((er,ec)) == player: er, ec = er+1, ec+1
        streak = tuple((r,c) for r,c in zip(
            range(sr+1,er), range(sc+1,ec)
        ))
        if len(streak) >= 5: return streak

        # /
        sr, er, sc, ec = row, row, col, col
        while self._data.get((sr,ec)) == player: sr, ec = sr-1, ec+1
        while self._data.get((er,sc)) == player: er, sc = er+1, sc-1
        streak = tuple((r,c) for r,c in zip(
            range(sr+1,er), reversed(range(sc+1,ec))
        ))
        if len(streak) >= 5: return streak

        return tuple()

    @property
    def last_pos(self):
        return self._last_pos

    @property
    def data(self):
        return self._data.items()