import pygame as pg
from tile import Tile


class Player(Tile):

    def __init__(self, pos: tuple, image: str, groups, obstacle_sprites) -> None:
        super().__init__(pos, image, groups)

        self.direction = pg.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.speed = 2

        self.__import_player_assets__()
        self.status = 'down'

        self.frame_index = 0
        self.animation_speed = 0.15

    def __import_player_assets__(self) -> None:
        spritesheet = pg.image.load('Graphics/Player/Skeleton.png').convert_alpha()

        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
        }

        self.animations['down_idle'].append(spritesheet.subsurface(pg.Rect(8,8,16,16)))
        self.animations['down_idle'].append(spritesheet.subsurface(pg.Rect(40,8,16,16)))
        self.animations['down_idle'].append(spritesheet.subsurface(pg.Rect(72,8,16,16)))
        self.animations['down_idle'].append(spritesheet.subsurface(pg.Rect(104,8,16,16)))

        self.animations['right_idle'].append(spritesheet.subsurface(pg.Rect(8,40,16,16)))
        self.animations['right_idle'].append(spritesheet.subsurface(pg.Rect(40,40,16,16)))
        self.animations['right_idle'].append(spritesheet.subsurface(pg.Rect(72,40,16,16)))
        self.animations['right_idle'].append(spritesheet.subsurface(pg.Rect(104,40,16,16)))

        self.animations['up_idle'].append(spritesheet.subsurface(pg.Rect(8,72,16,16)))
        self.animations['up_idle'].append(spritesheet.subsurface(pg.Rect(40,72,16,16)))
        self.animations['up_idle'].append(spritesheet.subsurface(pg.Rect(72,72,16,16)))
        self.animations['up_idle'].append(spritesheet.subsurface(pg.Rect(104,72,16,16)))

        self.animations['left_idle'].append(pg.transform.flip(self.animations['right_idle'][0],True,False))
        self.animations['left_idle'].append(pg.transform.flip(self.animations['right_idle'][1],True,False))
        self.animations['left_idle'].append(pg.transform.flip(self.animations['right_idle'][2],True,False))
        self.animations['left_idle'].append(pg.transform.flip(self.animations['right_idle'][3],True,False))

        self.animations['down'].append(spritesheet.subsurface(pg.Rect(8,104,16,16)))
        self.animations['down'].append(spritesheet.subsurface(pg.Rect(40,104,16,16)))
        self.animations['down'].append(spritesheet.subsurface(pg.Rect(72,104,16,16)))
        self.animations['down'].append(spritesheet.subsurface(pg.Rect(104,104,16,16)))
        
        self.animations['right'].append(spritesheet.subsurface(pg.Rect(8,136,16,16)))
        self.animations['right'].append(spritesheet.subsurface(pg.Rect(40,136,16,16)))
        self.animations['right'].append(spritesheet.subsurface(pg.Rect(72,136,16,16)))
        self.animations['right'].append(spritesheet.subsurface(pg.Rect(104,136,16,16)))

        self.animations['up'].append(spritesheet.subsurface(pg.Rect(8,168,16,16)))
        self.animations['up'].append(spritesheet.subsurface(pg.Rect(40,168,16,16)))
        self.animations['up'].append(spritesheet.subsurface(pg.Rect(72,168,16,16)))
        self.animations['up'].append(spritesheet.subsurface(pg.Rect(104,168,16,16)))

        self.animations['left'].append(pg.transform.flip(self.animations['right'][0],True,False))
        self.animations['left'].append(pg.transform.flip(self.animations['right'][1],True,False))
        self.animations['left'].append(pg.transform.flip(self.animations['right'][2],True,False))
        self.animations['left'].append(pg.transform.flip(self.animations['right'][3],True,False))

    def __animate__(self) -> None:
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_status(self) -> None:
        # idle status
        if self.direction.x == 0 and self.direction.y == 0 and 'idle' not in self.status:
            self.status += '_idle'

    def update(self) -> None:
        self.__input__()
        self.get_status()
        self.__animate__()
        self.__move__(self.speed)

    def __move__(self, speed) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.__collision__('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.__collision__('vertical')
        self.rect.center = self.hitbox.center

    def __collision__(self, direction) -> None:
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def __input__(self) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pg.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pg.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pg.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
