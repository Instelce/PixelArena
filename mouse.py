import pygame


class Mouse(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((10, 10))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=pygame.mouse.get_pos())
    
    def set_mouse(self, image):
        self.image = image

    def set_alpha(self, num):
        self.image.set_alpha(num)
    
    def update(self):
        self.rect = self.image.get_rect(topleft=pygame.mouse.get_pos())
        self.display_surface.blit(self.image, self.rect)