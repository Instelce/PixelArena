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
        self.pos = pos
        self.display_surface = pygame.display.get_surface()
        self.image = surface
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, 0)


class Relic(Object):
    def __init__(self, pos, groups, surface, enemies_sprite) -> None:
        super().__init__(pos, groups, surface)

        # Stats
        self.stats = {'health': 1000, 'attack': 10}
        self.health = self.stats['health']

        # Turret
        self.range_size = 1000
        self.range_rect = pygame.Rect(self.pos[0], self.pos[1], self.range_size, self.range_size)
        self.enemies_sprite = enemies_sprite

        # Damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invincibility_duration = 200
    
    def attack(self):
        # if self.health <= self.stats['health'] / 2:
        for enemy in self.enemies_sprite:
            if self.range_rect.collidepoint((enemy.rect.x, enemy.rect.y)):
                print("SHOOT ENEMY")
                pygame.draw.line(self.display_surface, "white", self.pos, enemy.rect.center, 2)

        # Drawing range
        pygame.draw.rect(self.display_surface, "white", self.range_rect, 4)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True
    
    def update(self):
        self.attack()
        self.cooldowns()