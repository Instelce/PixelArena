import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, groups, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface) -> None:
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = surface
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, 0)


class Relic(Object):
    def __init__(self, pos, groups, surface) -> None:
        super().__init__(pos, groups, surface)
        self.health = 100