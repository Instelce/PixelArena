import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.pos = pos

        self.image = pygame.Surface((32, 64))
        self.rect = self.image.get_rect(topleft=pos)

        # Movements
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 10
        self.gravity = 0.8
        self.jump_speed = -16

        # Player status
        self.current_x = 0
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.obstacle_sprites = obstacle_sprites

    def animate(self):
        # Set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.apply_gravity()
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # Right
                        self.rect.right = sprite.rect.left
                        self.on_right = True
                        self.current_x = self.rect.right
                    if self.direction.x < 0: # Left
                        self.rect.left = sprite.rect.right
                        self.on_left = True
                        self.current_x = self.rect.left
            
            # Reset on_right and on_left
            if self.on_right and (self.rect.right < self.current_x or self.direction.x <= 0):
                self.on_right = False
            elif self.on_left and (self.rect.left < self.current_x or self.direction.x >= 0):
                self.on_left = False

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # Down
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.on_ground = True
                    if self.direction.y < 0: # Up
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0
                        self.on_ceiling = True

            # Reset on_ground and on_ceiling
            if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
                self.on_ground = False
            elif self.on_ceiling and self.direction.y > 0:
                self.on_ceiling = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.animate()
        self.move(self.speed)

