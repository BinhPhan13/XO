import pygame as pg
from game import Game

BLACK = 0, 0, 0
WHITE = 240, 240, 240
GRAY = 200, 200, 200

class GridView:
    def __init__(self, width:int, height:int, cell_size:int):
        self._w = width * cell_size
        self._h = height * cell_size
        self._c = cell_size
        self._dx, self._dy = 0, 0

        self._load_imgs()
        self._game = Game()

    def _load_imgs(self):
        self._img_bd = self._c//min(self._c, 8)
        img_size = self._c - self._img_bd*2, self._c - self._img_bd*2

        img = pg.image.load('x.png')
        self._ximg = pg.transform.scale(img, img_size)

        img = pg.image.load('o.png')
        self._oimg = pg.transform.scale(img, img_size)

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

    def _move(self, dx, dy):
        if not (self._keys[pg.K_LCTRL]
            or self._keys[pg.K_RCTRL]): return

        if dx != 0: dx //= abs(dx)
        if dy != 0: dy //= abs(dy)

        accel = self._c//min(self._c, 5)
        self._dx += dx * accel
        self._dy += dy * accel

    def _mark_mouse(self):
        row, col = self._mouse2pos()
        sx, sy = self._pos2disp(row, col)
        pg.draw.rect(
            self._screen, GRAY,
            (sx+1, sy+1, self._c-1, self._c-1)
        )

    def _mouse2pos(self):
        mx, my = pg.mouse.get_pos()
        rx, ry = mx - self._dx, my - self._dy

        row = ry // self._c
        col = rx // self._c

        return row, col

    def _pos2disp(self, row, col):
        sx = col * self._c + self._dx
        sy = row * self._c + self._dy

        return sx, sy

    def _lclick(self):
        pos = self._mouse2pos()
        self._game.move(pos)

    def _draw_data(self):
        for pos, player in self._game.data:
            sx, sy = self._pos2disp(*pos)
            sx += self._img_bd
            sy += self._img_bd

            img = self._ximg if player > 0 else self._oimg
            self._screen.blit(img, (sx,sy))

    def mainloop(self):
        screen_size = self._w+1, self._h+1
        self._screen = pg.display.set_mode(screen_size)
        clock = pg.time.Clock()

        while True:
            self._screen.fill(WHITE)
            self._draw_grid()
            self._mark_mouse()
            self._draw_data()

            pg.display.flip()
            clock.tick(60)

            self._keys = pg.key.get_pressed()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("Bye...")
                    pg.quit()
                    return
                elif event.type == pg.MOUSEMOTION:
                    dx, dy = event.dict['rel']
                    self._move(dx, dy)
                elif event.type == pg.MOUSEBUTTONUP:
                    self._lclick()

if __name__ == '__main__':
    view = GridView(20, 12, 50)
    view.mainloop()