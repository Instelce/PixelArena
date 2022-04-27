import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.pos = pos

        self.image = pygame.Surface((16, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill('purple')

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -20

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_SPACE] and self.on_ground:
            self.jump(self.jump_speed)

    def jump(self, strenght):
        self.direction.y = strenght

    def update(self):
        self.get_input()