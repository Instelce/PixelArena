import pygame, math

from settings import *
from player import Player
from debug import debug
from tile import Tile, Object
from support import *
from mouse import Mouse
from enemy import Enemy
from weapon import Weapon


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.last_time = pygame.time.get_ticks()
        self.visible_sprites = YSortCameraGroup(WORLD_WIDTH, WORLD_HEIGHT)
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies_sprite = pygame.sprite.Group()

        self.mouse = Mouse()

        self.create_map()
        
        # Build
        self.in_build_mode = False
        self.build_range = (9 * TILE_SIZE, 6 * TILE_SIZE)
        self.build_range_rect = pygame.Rect(math.floor(SCREEN_WIDTH/2 - self.build_range[0]/2),math.floor(SCREEN_HEIGHT/2 - self.build_range[1]/2), self.build_range[0], self.build_range[1])
        # self.build_block = pygame.image.load('graphics/player/build/block.png').convert_alpha()
        self.build_block = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.build_block.fill('gray')
        self.can_build = True
    
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
            'terrain': import_csv_layout('map/map_1_terrain.csv'),
            'player': import_csv_layout('map/map_1_player.csv'),
            'enemy': import_csv_layout('map/map_1_enemy.csv'),
            'objects': import_csv_layout('map/map_1_objects.csv'),
        }
        graphics = {
            'terrain': import_cut_graphics('graphics/terrain.png'),
            'objects': import_folder('../graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'terrain':
                            surf = graphics['terrain'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], surf)
                        if style == 'player':
                            self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack)
                        # if style == 'enemy':
                        #     Enemy((x, y), [self.visible_sprites, self.enemies_sprite], self.obstacle_sprites, self.player)
                        if style == 'objects':
                            surf = pygame.image.load("graphics/objects/relique.png").convert_alpha()
                            Object((x, y), [self.visible_sprites, self.obstacle_sprites], surf)

    # BUILD
    def build(self):
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        build_cursor_border = 2

        # Preview
        # build_preview = pygame.image.load('graphics/player/build/block.png')
        # build_preview.set_alpha(100)
        
        # Draw build range
        pygame.draw.rect(self.display_surface, "blue", self.build_range_rect, 2)

        # Draw grid tile
        for tile in self.grid_tiles:
            if tile.collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, "red", tile, build_cursor_border)      
                self.grid_tile_selected = tile              
                
                if tile.colliderect(self.build_range_rect) and not tile.colliderect(self.player.rect):
                    # Can build
                    # self.display_surface.blit(build_preview, (tile.x, tile.y))
                    pygame.draw.rect(self.display_surface, "white", tile, build_cursor_border)

                    offset_pos = self.visible_sprites.get_offset_pos(self.player, (self.grid_tile_selected.x, self.grid_tile_selected.y), sign='+')

                    # Place block
                    if pygame.mouse.get_pressed()[0] and self.can_build and now - self.last_time >= 100:
                        print(f"BUILD A BLOCK : {offset_pos}")
                        self.last_time = now
                        
                        Tile(offset_pos, [self.visible_sprites, self.obstacle_sprites], self.build_block)
                    
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
                offset_pos = self.visible_sprites.get_offset_pos(self.player, (x,y))
                tile = pygame.Rect(offset_pos[0], offset_pos[1], TILE_SIZE, TILE_SIZE)
                self.grid_tiles.append(tile)
    
    # ATTACK
    def create_attack(self):
        Weapon(self.player, [self.visible_sprites])

    def run(self):
        # Update and draw the game
        self.input()

        if self.in_build_mode:
            self.create_build_grid()
            self.build()

        self.visible_sprites.update()
        self.visible_sprites.set_target(self.player)

        self.mouse.update()

        # Debug
        debug(pygame.mouse.get_pos())
        debug(self.player.direction, 20)
        debug(f"on_ground : {self.player.on_bottom}", 30)
        debug(self.player.rect.topleft, 40)
        debug(self.player.speed, 50)
        # debug(f"selected tile pos : {self.grid_tile_selected.x}, {self.grid_tile_selected.y}", 50)
        debug(f"in_build_mode : {self.in_build_mode}", 60)
        debug(f"player.direction : {self.player.direction}", 70)


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

        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target_rect):
        return target_rect.move(self.state.topleft)

    def complex_camera(self, camera, target):
        # we want to center target_rect
        x = -target.rect.center[0] + SCREEN_WIDTH / 2
        y = -target.rect.center[1] + SCREEN_HEIGHT / 2
        # move the camera. Let's use some vectors so we can easily substract/multiply
        # add some smoothness coolnes
        camera.topleft += (pygame.Vector2((x, y)) -
                           pygame.Vector2(camera.topleft)) * 0.06
        # set max/min x/y so we don't see stuff outside the world
        camera.x = max(-(camera.width - SCREEN_WIDTH), min(0, camera.x))
        camera.y = max(-(camera.height - SCREEN_HEIGHT), min(0, camera.y))

        return camera

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

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)