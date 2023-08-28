import pygame as pg
from settings import *


class Tile(pg.sprite.Sprite):

    def __init__(self, pos: tuple, image: str, groups) -> None:
        super().__init__(groups)
        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4,-5)
