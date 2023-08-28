import pygame as pg
import sys
from settings import *
from level import Level

class Game:

    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption("Pycman")
        self.clock = pg.time.Clock()

        self.level = Level()

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
            self.screen.fill("black")
            self.level.run()
            pg.display.update()
            self.clock.tick(SPEED)


if __name__ == "__main__":
    game = Game()
    game.run()