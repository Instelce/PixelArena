import pygame
from random import choice
from math import floor

from enemy import Enemy
from settings import TILE_SIZE


class Spawner(pygame.sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.pos = pos
        self.display_surface = pygame.display.get_surface()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill('orange')

    def enemy_spawn(self, enemy_name, pos, groups, obstacle_sprites, damage_player):
        Enemy(enemy_name, pos, groups, obstacle_sprites, damage_player)


class Wave:
    def __init__(self, start_difficulty, spawners_sprite) -> None:
        self.difficulty = start_difficulty
        self.spawners_sprite = spawners_sprite

        self.start_duration = 20 # Secondes
        self.min_enemies_number = 2
        self.current_time = 0
        self.last_time_wave = pygame.time.get_ticks() 
        self.last_time = pygame.time.get_ticks() 

        self.is_finish = False

        self.enemy_list = ['bamboo', 'slimevampire', 'spirit', 'squid']

        self.set_difficulty(self.difficulty)
    
    def __del__(self):
        self.current_time = 0

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.duration = self.difficulty * self.start_duration * 1000
        self.enemies_number = self.difficulty * self.min_enemies_number
        self.enemies_spawn_counter = 0
        self.spawn_cooldown = floor(self.duration / self.enemies_number)
        self.cooldown = self.spawn_cooldown

    def check_spawn(self, enemy_groups, obstacle_sprites, damage_player):
        if self.current_time >= self.cooldown and self.enemies_spawn_counter <= self.enemies_number:
            self.cooldown += self.spawn_cooldown
            
            now = pygame.time.get_ticks()
            if now - self.last_time >= 10:
                self.last_time = now
                for spawner in self.spawners_sprite:
                    spawner.enemy_spawn(choice(self.enemy_list), spawner.pos, enemy_groups, obstacle_sprites, damage_player)
            
            self.enemies_spawn_counter += 1

    def start(self):
        now = pygame.time.get_ticks()
        if now - self.last_time_wave >= 10:
            self.last_time_wave = now
            self.current_time += 100

        if self.current_time >= self.duration:
            self.is_finish = True

        print('Timer', self.current_time, '/', self.duration)
        print('Cooldown', self.spawn_cooldown, '/', self.cooldown)
        print('Enemies number', self.enemies_number)
        print('Counter', self.enemies_spawn_counter)
        print('Difficulty', self.difficulty, '|')
        print()

