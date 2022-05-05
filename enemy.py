from re import S
import pygame


from entity import Entity


class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, player) -> None:
        super().__init__(pos, groups, obstacle_sprites)
        self.player = player

        self.image = pygame.Surface((32, 64))
        self.image.fill('gray')
        self.speed = 4

    def get_direction(self, start_pos, end_pos):
        start = pygame.math.Vector2(start_pos)
        end = pygame.math.Vector2(end_pos)
        print((start - end).normalize())
        return (end - start).normalize()
    
    def track_player(self):
        self.player_vector = self.get_direction(self.rect.x, self.player.rect.x)
        self.direction = self.player_vector

    def update(self):
        self.track_player()
        self.move(self.speed)