import pygame as pg

BLACK = 0, 0, 0
WHITE = 240, 240, 240
GRAY = 200,200,200

MOVEMENTS = {
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
}

class GridView:
    def __init__(self, width:int, height:int, cell_size:int):
        self._w = width * cell_size
        self._h = height * cell_size
        self._c = cell_size
        self._dx, self._dy = 0, 0

    def _draw_grid(self):
        sx = self._dx % self._c
        sy = self._dy % self._c

        for x in range(sx, self._w+1, self._c):
            pg.draw.line(
                self._screen, BLACK,
                (x,0), (x,self._h)
            )
        for y in range(sy, self._h+1, self._c):
            pg.draw.line(
                self._screen, BLACK,
                (0,y), (self._w,y)
            )

    def _move(self, key):
        dx, dy = MOVEMENTS[key]

        accel = self._c//5
        self._dx += dx * accel
        self._dy += dy * accel

    def _mark_mouse(self):
        mx, my = pg.mouse.get_pos()
        sx, sy = self._abs2topleft(mx, my)
        pg.draw.rect(
            self._screen, GRAY,
            (sx+1, sy+1, self._c-1, self._c-1)
        )

    def _abs2topleft(self, x, y):
        a, b = divmod(x, self._c)
        k = self._dx % self._c
        if b < k: a -= 1
        sx = a * self._c + k

        a, b = divmod(y, self._c)
        k = self._dy % self._c
        if b < k: a -= 1
        sy = a * self._c + k

        return sx, sy

    def mainloop(self):
        screen_size = self._w+1, self._h+1
        self._screen = pg.display.set_mode(screen_size)
        clock = pg.time.Clock()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("Bye...")
                    pg.quit()
                    return

            self._screen.fill(WHITE)
            self._draw_grid()
            self._mark_mouse()

            keys = pg.key.get_pressed()
            for k in MOVEMENTS:
                if keys[k]: self._move(k)

            pg.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    view = GridView(7, 5, 100)
    view.mainloop()