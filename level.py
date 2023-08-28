import itertools
import pygame as pg
import random as rnd

from settings import *
from player import Player
from tile import Tile


class Level:
    def __init__(self, surface) -> None:

        self.visible_sprites = YSortCameraGroup(surface)
        self.obstacle_sprites = YSortCameraGroup(surface)

        self.display_surface = surface

        self.images = {
            "wall": "Graphics/Tiles/010.png",
            "floor": "Graphics/Tiles/015.png",
            "player": "Graphics/Player/pacplay.png"
        }

        self.__create_level__()

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


    def __create_level__(self) -> None:
        level = self.__generate_labyrinth__()
        for row_index, row in enumerate(level):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 1:
                    Tile((x, y), self.images["wall"], [
                         self.visible_sprites, self.obstacle_sprites])

        self.player = Player((LEVEL_SIZE//2*TILESIZE, LEVEL_SIZE//2*TILESIZE),
                             self.images["player"], [self.visible_sprites], self.obstacle_sprites)

    def __generate_labyrinth__(self) -> list:
        size = LEVEL_SIZE
        center = (size//2, size//2)

        grid = self.__gen_grid__(size)
        self.__destroy_wall__(grid, center, size//2)

        for y, x in itertools.product(range(size//2-2, size//2+3), range(size//2-2, size//2+3)):
            grid[y][x] = 0

        return grid

    def __destroy_wall__(self, grid: list, center: tuple, size: int) -> None:
        if size < 2:
            return

        directions = rnd.sample(range(4), 3)

        for x in directions:
            if x == 0:
                steps = rnd.randrange(1, size, 2)
                grid[center[0]+steps][center[1]] = 0
            elif x == 1:
                steps = rnd.randrange(1, size, 2)
                grid[center[0]][center[1]+steps] = 0
            elif x == 2:
                steps = rnd.randrange(1, size, 2)
                grid[center[0]-steps][center[1]] = 0
            elif x == 3:
                steps = rnd.randrange(1, size, 2)
                grid[center[0]][center[1]-steps] = 0
            else:
                print("This shouldn't happen. How the fuck did we get here?")
                exit(1)

        newsize = size//2
        newCenters = [(center[0]+newsize, center[1]+newsize),
                      (center[0]-newsize, center[1]+newsize),
                      (center[0]-newsize, center[1]-newsize),
                      (center[0]+newsize, center[1]-newsize)]
        for x in newCenters:
            self.__destroy_wall__(grid, x, newsize)

    def __gen_grid__(self, size: list) -> list:
        retgrid = [[1 for _ in range(size)] for _ in range(size)]

        for y in range(size):
            if y % 2 == 1:
                for x in range(size):
                    if x % 2 == 1:
                        retgrid[y][x] = 0

        return retgrid


class YSortCameraGroup(pg.sprite.Group):
    def __init__(self, surface) -> None:
        super().__init__()

        self.display_surface = surface
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pg.math.Vector2()



    def custom_draw(self, player) -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
