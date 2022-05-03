import pygame

from tile import Tile
from support import *
from settings import *
from debug import debug
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(pos, groups, obstacle_sprites)
        self.image.fill('purple')

        self.speed = 10

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            print("PLAYER JUMP")
            self.jump()

    def update(self):
        self.input()
        self.animate()
        self.move(self.speed)