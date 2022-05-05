import pygame

from tile import Tile
from support import *
from settings import *
from debug import debug
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack) -> None:
        super().__init__(pos, groups, obstacle_sprites)
        self.image.fill('purple')

        self.speed = 5

        self.last_time = pygame.time.get_ticks()

        # Movements
        self.speed = 10
        self.jump_size = -20
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.accelerate()
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
            self.accelerate()
        else:
            self.speed = 5
            self.direction.x = 0

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.accelerate()
        elif keys[pygame.K_UP] or keys[pygame.K_z]:
            self.direction.y = -1
            self.accelerate()
        else:
            self.speed = 5
            self.direction.y = 0

    def accelerate(self):
        now = pygame.time.get_ticks()

        if now - self.last_time >= 150 and self.speed < 10:
            self.last_time = now
            self.speed += 1
            print(self.speed)

    def update(self):
        self.input()
        self.animate()
        self.move(self.speed)