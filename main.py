import pygame
import sys

from settings import *
from level import Level
from menu import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Pixel Arena")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.status = 'start_menu'
        # self.status = 'game'

        self.level = Level()
        self.start_menu = Menu('simple_menu',
                               "Pixel Arena",
                               [
                                   Text("PIXEL ARENA",
                                        UI_FONT,
                                        40,
                                        "white",
                                        (SCREEN_WIDTH / 2, 200)),
                                   Button("Start", None,
                                          (SCREEN_WIDTH / 2, 0)),
                                   Button("Shop", None, (SCREEN_WIDTH / 2, 0)),
                                   Button("Settings", None,
                                          (SCREEN_WIDTH / 2, 0)),
                                   Button("Quit", None, (SCREEN_WIDTH / 2, 0)),
                               ],
                               "graphics/ui/background.png")

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
            else:
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
