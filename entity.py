import pygame
from math import sin

from settings import TILE_SIZE


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()

        # Movements
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2(0, 0)

        self.on_right = False
        self.on_left = False
        self.on_bottom = False
        self.on_top = False

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        # Vertical
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Right
                        self.hitbox.right = sprite.hitbox.left
                        self.on_right = True
                        self.current_x = self.hitbox.right
                    if self.direction.x < 0:  # Left
                        self.hitbox.left = sprite.hitbox.right
                        self.on_left = True
                        self.current_x = self.hitbox.left

            # Reset on_right and on_left
            if self.on_right and (self.hitbox.right < self.current_x or self.direction.x <= 0):
                self.on_right = False
            elif self.on_left and (self.hitbox.left < self.current_x or self.direction.x >= 0):
                self.on_left = False

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Down
                        self.hitbox.bottom = sprite.hitbox.top
                        self.on_bottom = True
                    if self.direction.y < 0:  # Up
                        self.hitbox.top = sprite.hitbox.bottom
                        self.on_top = True

            # Reset on_bottom and on_top
            if self.on_bottom and self.direction.y < 0 or self.direction.y > 1:
                self.on_bottom = False
            elif self.on_top and self.direction.y > 0:
                self.on_top = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
