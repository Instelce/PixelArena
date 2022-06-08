from math import floor

from menu.components import *
from settings import *


class SceneTransition:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.last_time = pygame.time.get_ticks()

        self.size = 0

        self.transition_is_finish = False
        self.can_dicrease = False
        self.cooldown = 1
        self.grow = 100

    def start(self, status):
        self.loading_text = Text('center', "Pixel Arena", UI_FONT, floor(self.size/20), 'white', (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        if self.transition_is_finish:
            self.transition_is_finish = False
            self.can_dicrease = False
            self.size = 100

        max_size = SCREEN_WIDTH + (SCREEN_WIDTH/3)

        current_time = pygame.time.get_ticks()

        if not self.transition_is_finish:
            if self.size <= max_size:
                if current_time - self.last_time >= self.cooldown:
                    self.last_time = current_time
                    self.size += self.grow

                    # print('increase')
                    # print('size', self.size)

                    if self.size >= max_size:
                        self.can_dicrease = True

            pygame.draw.rect(self.display_surface, 'black', pygame.Rect(0, 0, self.size, SCREEN_HEIGHT))
            
            if self.size >= SCREEN_WIDTH/2:
                self.loading_text.display()

    def end(self, status):
        self.loading_text = Text('center', "Pixel Arena", UI_FONT, floor(self.size/20), 'white', (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        if not self.transition_is_finish:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.last_time >= self.cooldown:
                self.last_time = current_time
                self.size -= self.grow

                # print("dicrease")
                # print('size', self.size)

                if self.size <= 0:
                    self.size = 0
                    self.transition_is_finish = True

            pygame.draw.rect(self.display_surface, 'black', pygame.Rect(SCREEN_WIDTH-self.size, 0, self.size, SCREEN_HEIGHT))
            
            if self.size >= SCREEN_WIDTH/2:
                self.loading_text.display()