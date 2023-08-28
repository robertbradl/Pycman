import pygame as pg
import sys
from settings import *
from level import Level

class Game:

    def __init__(self) -> None:
        pg.init()

        self.display_screen = pg.display.set_mode((WIDTH*3,HEIGHT*3))
        self.screen = pg.Surface((HEIGHT,WIDTH))
        pg.display.set_caption("Pycman")
        self.clock = pg.time.Clock()

        self.level = Level(self.screen)

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
            self.screen.fill("black")
            
            self.level.run()
            scaled_screen = pg.transform.smoothscale(self.screen, self.display_screen.get_size())
            self.display_screen.blit(scaled_screen, (0,0))
            pg.display.flip()
            self.clock.tick(SPEED)


if __name__ == "__main__":
    game = Game()
    game.run()