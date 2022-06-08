import pygame


from entity import Entity
from settings import *
from support import *


class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites, damage_player, damage_relic) -> None:
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Graphic setup
        self.import_graphics(enemy_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # Movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.enemy_name = enemy_name
        enemy_info = enemy_data[self.enemy_name]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']

        # Player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.damage_relic = damage_relic

        # Invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f"graphics/enemies/{name}/"

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_object_or_entity_distance_direction(self, object_or_entity):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        object_or_entity_vec = pygame.math.Vector2(object_or_entity.rect.center)

        distance = (object_or_entity_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (object_or_entity_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player, relic):
        player_distance = self.get_object_or_entity_distance_direction(player)[0]
        relic_distance = self.get_object_or_entity_distance_direction(relic)[0]

        if player_distance <= self.attack_radius and self.can_attack:
            # if self.status != 'attack':
            #     self.frame_index = 0
            self.status = 'attack_player'
            self.can_attack = False
        elif relic_distance <= self.attack_radius and self.can_attack:
            self.status = 'attack_relic'
            self.can_attack = False
        elif player_distance <= self.notice_radius:
            self.status = 'move_to_player'
        else:
            self.status = 'move_to_relic'

    def actions(self, player, relic):
        if self.status == 'attack_player':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'attack_relic':
            self.attack_time = pygame.time.get_ticks()
            self.damage_relic(self.attack_damage, self.attack_type)
        elif self.status == 'move_to_player':
            self.direction = self.get_object_or_entity_distance_direction(player)[1]
        elif self.status == 'move_to_relic':
            self.direction = self.get_object_or_entity_distance_direction(relic)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status.split('_')[0]]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Flicker
        if not self.vulnerable:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_object_or_entity_distance_direction(player)[1]

            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                pass # Magic damage

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player, relic):
        self.get_status(player, relic)
        self.actions(player, relic)
