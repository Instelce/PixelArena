import pygame


from settings import *
from player import Player
from debug import debug
from tile import Tile
from support import *


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        # self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        layouts = {
            'terrain': import_csv_layout('map/map_1_terrain.csv'),
            'player': import_csv_layout('map/map_1_player.csv'),
        }
        graphics = {
            'block': import_folder('../graphics/block.png'),
            'grass': import_folder('../graphics/Grass'),
            'objects': import_folder('../graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'terrain':
                            surf = graphics['block']
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], surf)
                        if style == 'player':
                            self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # Update and draw the game
        self.visible_sprites.custom_draw(self.player)
        # self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:

        # General setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)