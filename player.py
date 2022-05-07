import pygame

from tile import Tile
from support import *
from settings import *
from debug import debug
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic) -> None:
        super().__init__(pos, groups, obstacle_sprites)
        self.image.fill('purple')
        self.hitbox = self.rect.inflate(0, -60)

        # Graphics setup
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.last_time = pygame.time.get_ticks()

        # Movements
        self.jump_size = -20
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
        'up_idle': [],'down_idle': [],'left_idle': [],'right_idle': [],
        'up_attack': [],'down_attack': [],'left_attack': [],'right_attack': [],}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_csv_layout(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # X axis
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                # self.accelerate()
                self.status = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.direction.x = -1
                # self.accelerate()
                self.status = 'left'
            else:
                self.speed = 5
                self.direction.x = 0

            # Y axis
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                # self.accelerate()
                self.status = 'down'
            elif keys[pygame.K_UP] or keys[pygame.K_z]:
                self.direction.y = -1
                # self.accelerate()
                self.status = 'up'
            else:
                self.speed = 5
                self.direction.y = 0
            
            # Attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # Magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strenght = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strenght, cost)

            # Switch weapons input
            if keys[pygame.K_x] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):

        # Idle status
        if self.direction.x  == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.animations[self.status]

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def accelerate(self):
        now = pygame.time.get_ticks()

        if now - self.last_time >= 150 and self.speed < 10:
            self.last_time = now
            self.speed += 1
            print(self.speed)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def update(self):
        self.input()
        # self.animate()
        self.cooldowns()
        self.get_status()
        self.move(self.speed)