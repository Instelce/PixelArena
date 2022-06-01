import pygame
import sys

from settings import *
from level import Level
from menu import *
from shop import Shop
from debug import debug
from api import Api
from support import read_json_file, write_json_file


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Pixel Arena")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player_data = read_json_file("data/player.json")
        self.api = Api()

        # Scenes
        if self.api.is_authenticate:
            self.api.download_data()
            self.create_loading_page()
        else:
            self.status = 'login_menu'
        self.old_status = self.status

        self.scene_transition = SceneTransition()
        self.scenes = {
            'loading_page': Menu('simple_menu',
                                 [
                                     Text('center',
                                        "Pixel Arena",
                                        UI_FONT,
                                        TITLE_FONT_SIZE,
                                        "white",
                                        (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100)),
                                    LoadingBar(self.api.tasks, self.create_start_menu)
                                 ],
                                 "graphics/ui/background.png"
                                 ),
            'login_menu': Menu('simple_menu',
                               [
                                   Text('center',
                                        "Login",
                                        UI_FONT,
                                        TITLE_FONT_SIZE,
                                        "white",
                                        (SCREEN_WIDTH/2, 200)),
                                   Input("Username"),
                                   Input("Password"),
                                   Button("Login", self.login,
                                          (SCREEN_WIDTH/2, 200), 50),
                               ],
                               "graphics/ui/background.png"
                               ),
            'start_menu': Menu('simple_menu',
                               [
                                   Text("center",
                                        "PIXEL ARENA",
                                        UI_FONT,
                                        TITLE_FONT_SIZE,
                                        "white",
                                        (SCREEN_WIDTH / 2, 100)),
                                   Text("center",
                                        f"Login with {self.player_data['username']} account",
                                        UI_FONT,
                                        UI_FONT_SIZE,
                                        "white",
                                        (SCREEN_WIDTH / 2, 100)),
                                   Button("Start", self.create_level),
                                   Button("Shop", self.create_shop),
                                   Button("Settings", None),
                                   Button("Disconnect", self.disconnect, None),
                                   Button("Quit", self.quit, None),
                               ],
                               "graphics/ui/background.png"),
            'shop': Shop('shop',
                         [
                             Text("center",
                                  "SHOP",
                                  UI_FONT,
                                  TITLE_FONT_SIZE,
                                  "white",
                                  (SCREEN_WIDTH / 2, 50),
                                  ),
                         ],
                         "graphics/ui/background.png",
                         self.create_start_menu
                         ),
            'level': Level()
        }

    def create_start_menu(self):
        self.status = 'start_menu'
    
    def create_loading_page(self):
        self.status = 'loading_page'

    def create_shop(self):
        self.status = 'shop'

    def create_level(self):
        self.status = 'level'

    def login(self):
        username = self.scenes[self.status].components[1].value
        password = self.scenes[self.status].components[2].value
        self.api.authenticate(username, password)

        try:
            self.api.authenticate(username, password)
        except ValueError:
            self.status = 'login_menu'
            self.scenes[self.status].components[1].value = ""
            self.scenes[self.status].components[2].value = ""
        
        if self.api.is_authenticate:
            self.api.download_data()
            self.status = 'loading_page'

        self.player_data = read_json_file("data/player.json")
            

    def disconnect(self):
        write_json_file("data/player.json", {
            'username': "",
            'token': "",
        })
        self.status = 'login_menu'

    def quit(self):
        pygame.quit()
        sys.exit()

    def display_scene(self):
        if self.old_status != self.status:
            self.scenes[self.old_status].display()
            self.scene_transition.start(self.status)

            if self.scene_transition.can_dicrease:
                self.old_status = self.status

        if self.old_status == self.status:
            self.scenes[self.status].display()
            self.scene_transition.end(self.status)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((12, 12, 12))
            self.display_scene()

            debug(pygame.mouse.get_pos())

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
