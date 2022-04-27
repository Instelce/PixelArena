import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('graphics/block.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)