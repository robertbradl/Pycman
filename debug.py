import pygame as pg

pg.init()

font = pg.font.FontType(None, 30)


def debug(info,surface, y=10, x=10) -> None:
    display_surface = surface
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pg.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)
