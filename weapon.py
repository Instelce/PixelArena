import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        super().__init__(groups)
        direction = pygame.math.Vector2()
        
        # Graphics
        self.image = pygame.Surface((40, 40))
        
        # Placements
        self.rect = self.image.get_rect(center=player.rect.center)