import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.pos = pos

        self.image = pygame.Surface((32, 64))
        self.rect = self.image.get_rect(topleft=pos)
        # self.hitbox = self.rect.inflate(0, 0)
        self.image.fill('purple')

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -20

        self.obstacle_sprites = obstacle_sprites

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            self.jump(self.jump_speed)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        
        if direction == 'vertical':
            self.apply_gravity()

            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed 
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self, strenght):
        self.direction.y = strenght

    def update(self):
        self.get_input()
        self.move(self.speed)