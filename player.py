import pygame as pg
from tile import Tile


class Player(Tile):

    def __init__(self, pos: tuple, image: str, groups, obstacle_sprites) -> None:
        super().__init__(pos, image, groups)

        self.direction = pg.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.speed = 2

    def update(self) -> None:
        self.__input__()
        self.__move__(self.speed)

    def __move__(self, speed) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.__collision__('horizontal')
        self.rect.y += self.direction.y * speed
        self.__collision__('vertical')


    def __collision__(self, direction) -> None:
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom

    def __input__(self) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.direction.y = -1
        elif keys[pg.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_a]:
            self.direction.x = -1
        elif keys[pg.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
