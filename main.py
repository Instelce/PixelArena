import pygame
import sys

from settings import *
from level import Level
from menu import *
from shop import Shop


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Pixel Arena")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.status = 'shop'
        # self.status = 'game'

        self.level = Level()
        self.shop = Shop('shop',
                         [
                             Text("SHOP",
                                  UI_FONT,
                                  TITLE_FONT_SIZE,
                                  "white",
                                  (SCREEN_WIDTH / 2, 50),
                                  ),
                         ],
                         "graphics/ui/background.png"
                         )
        self.start_menu = Menu('simple_menu',
                               [
                                   Text("PIXEL ARENA",
                                        UI_FONT,
                                        TITLE_FONT_SIZE,
                                        "white",
                                        (SCREEN_WIDTH / 2, 200)),
                                   Button("Start", self.create_level,
                                          (SCREEN_WIDTH / 2, 0)),
                                   Button("Shop", None, (SCREEN_WIDTH / 2, 0)),
                                   Button("Settings", None,
                                          (SCREEN_WIDTH / 2, 0)
                                          ),
                                   Button("Quit", self.quit, (SCREEN_WIDTH / 2, 0),
                                          80),
                               ],
                               "graphics/ui/background.png")

    def create_level(self):
        self.level = Level()
        self.status = 'game'

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((12, 12, 12))

            # Display scene
            if self.status == 'start_menu':
                self.start_menu.display()
            elif self.status == 'shop':
                self.shop.display()
            else:
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
