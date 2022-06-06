import pygame
import math

from settings import *
from player import Player
from debug import debug
from spawner import Spawner, Wave
from tile import Relic, Tile, Object
from support import *
from mouse import Mouse
from enemy import Enemy
from ui import UI
from weapon import Weapon
from particles import AnimationPlayer


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.last_time = pygame.time.get_ticks()
        self.visible_sprites = YSortCameraGroup(WORLD_WIDTH, WORLD_HEIGHT)
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies_sprite = pygame.sprite.Group()

        self.mouse = Mouse()

        # Spawner and wave
        self.spawners_sprite = pygame.sprite.Group()
        self.wave_difficulty = 1
        self.current_wave = Wave(self.wave_difficulty, self.spawners_sprite)

        # Build
        self.in_build_mode = False
        self.build_range = (9 * TILE_SIZE, 6 * TILE_SIZE)
        self.build_range_rect = pygame.Rect(math.floor(SCREEN_WIDTH / 2 - self.build_range[0] / 2), math.floor(
            SCREEN_HEIGHT / 2 - self.build_range[1] / 2), self.build_range[0], self.build_range[1])
        self.build_block = pygame.image.load(
            'graphics/player/build/block.png').convert_alpha()
        self.can_build = True

        # Attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # User interface
        self.ui = UI()

        # Particles
        self.animation_player = AnimationPlayer()

        self.create_map()

    def input(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if keys[pygame.K_b] and now - self.last_time >= 400:
            self.last_time = now
            if self.in_build_mode:
                self.in_build_mode = False
            elif not self.in_build_mode:
                self.in_build_mode = True

    def create_map(self):
        layouts = {
            'wall': import_csv_layout('map/map_1_wall.csv'),
            'grass': import_csv_layout('map/map_1_grass.csv'),
            'stone_ground': import_csv_layout('map/map_1_stone_ground.csv'),
            'entities': import_csv_layout('map/map_1_entities.csv'),
            'objects': import_csv_layout('map/map_1_objects.csv'),
        }
        graphics = {
            'wall': import_cut_graphics('graphics/terrain/wall.png'),
            'grass': import_cut_graphics('graphics/terrain/grass.png'),
            'objects': import_folder('graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE

                        if style == 'wall':
                            surf = graphics['wall'][int(col)]
                            Tile("wall", (x, y), [self.visible_sprites,
                                                  self.obstacle_sprites], surf)
                        if style == 'objects':
                            if col == '1':
                                surf = graphics['objects'][0]
                                self.relic = Relic((x, y), [self.visible_sprites, self.obstacle_sprites], surf)
                        if style == 'entities':
                            if col == '0':
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == '4':
                                    Spawner((x, y),
                                        [self.spawners_sprite, self.visible_sprites])
                        # if style == 'grass':
                        #     surf = graphics['grass'][int(col)]
                        #     Tile("grass", (x, y), [self.visible_sprites], surf)

    # BUILD
    def build(self):
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        build_cursor_border = 2

        # Preview
        build_preview = pygame.image.load('graphics/player/build/block.png')
        build_preview.set_alpha(100)

        # Draw build range
        pygame.draw.rect(self.display_surface, "blue",
                         self.build_range_rect, 2)

        # Draw grid tile
        for tile in self.grid_tiles:
            if tile.collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, "red",
                                 tile, build_cursor_border)
                self.grid_tile_selected = tile

                if tile.colliderect(self.build_range_rect) and not tile.colliderect(self.player.rect):
                    # Can build
                    self.display_surface.blit(build_preview, (tile.x, tile.y))
                    pygame.draw.rect(self.display_surface,
                                     "white", tile, build_cursor_border)

                    offset_pos = self.visible_sprites.get_offset_pos(
                        self.player, (self.grid_tile_selected.x, self.grid_tile_selected.y), sign='+')

                    # Place block
                    if pygame.mouse.get_pressed()[0] and self.can_build and now - self.last_time >= 100:
                        print(f"BUILD A BLOCK : {offset_pos}")
                        self.last_time = now

                        Tile("build_block", offset_pos, [self.visible_sprites,
                                                         self.obstacle_sprites], self.build_block)

                    # Destroy block
                    if pygame.mouse.get_pressed()[2]:
                        print(f"DESTROY A BLOCK : {offset_pos}")

                        for sprite in self.obstacle_sprites:
                            if sprite.rect.collidepoint(offset_pos):
                                sprite.kill()

    def create_build_grid(self):
        self.grid_tiles = []
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            for y in range(0, WORLD_HEIGHT, TILE_SIZE):
                offset_pos = self.visible_sprites.get_offset_pos(
                    self.player, (x, y))
                tile = pygame.Rect(
                    offset_pos[0], offset_pos[1], TILE_SIZE, TILE_SIZE)
                self.grid_tiles.append(tile)

    # WEAPON and MAGIC
    def create_attack(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False)

                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def wave_management(self):
        if self.current_wave.is_finish:
            self.wave_difficulty += 1

            del self.current_wave
            self.current_wave = Wave(self.wave_difficulty, self.spawners_sprite)

        self.current_wave.start()
        self.current_wave.check_spawn([self.visible_sprites, self.enemies_sprite, self.attackable_sprites], self.obstacle_sprites, self.damage_player)


    def display(self):
        # Update and draw the game
        self.input()
        self.wave_management()

        if self.in_build_mode:
            self.create_build_grid()
            self.build()

        self.visible_sprites.set_target(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player, self.relic)

        self.player_attack_logic()

        self.ui.display(self.player, self.current_wave)
        self.mouse.update()

        # Debug
        debug(self.player.direction, 20)
        debug(f"on_ground : {self.player.on_bottom}", 30)
        debug(self.player.rect.topleft, 40)
        debug(f"player.speed : {self.player.speed}", 50)
        debug(f"in_build_mode : {self.in_build_mode}", 60)
        debug(f"player.direction : {self.player.direction}", 70)
        debug(f"player.status : {self.player.status}", 80)
        debug(f"len(self.enemies_sprite) : {len(self.enemies_sprite)}", 80)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, width, height) -> None:

        # General setup
        super().__init__()
        self.width = width
        self.height = height
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.background = pygame.image.load(
            "map/map_1_grass.png").convert_alpha()

    def get_offset_pos(self, player, pos, sign="-"):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        if sign == '-':
            offset_pos = pos - self.offset
        else:
            offset_pos = pos + self.offset

        return offset_pos

    def set_target(self, player):
        # self.state = self.complex_camera(self.state, player)

        # Getting the offset
        # self.offset.x = max(-(self.width - SCREEN_WIDTH), min(0, self.offset.x))
        # self.offset.y = max(-(self.height - SCREEN_HEIGHT), min(0, self.offset.y))
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        self.display_surface.blit(self.background, (0, 0) - self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player, relic):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, relic)
