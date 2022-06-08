import pygame
from math import floor

from menu.components import *
from settings import *


class Menu:
    def __init__(self, menu_type, components, background) -> None:
        self.menu_type = menu_type
        self.components = components
        self.background = pygame.transform.scale(
            pygame.image.load(background).convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.display_surface = pygame.display.get_surface()

    def components_reposition(self):
        positionned = False

        if not positionned:
            start_pos = list(self.components[0].pos)

            for i in range(len(self.components)):
                if i >= 1:
                    component = self.components[i]
                    component_pos = list(component.pos)
                    component_size = list(self.components[i].size)
                    # print(start_pos, component_pos, component_size)

                    # Repos
                    new_pos = start_pos[1] + \
                        component_size[1] + component.margin * i
                    component_pos[1] = new_pos
                    component.pos = tuple(component_pos)

                positionned = True

    def display_components(self):
        for component in self.components:
            component.display()

    def draw_text(self, text, font, font_size, color, pos):
        font = pygame.font.Font(font, font_size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(midtop=pos)
        self.display_surface(text_surf, text_rect)

    def display(self):
        self.components_reposition()

        self.display_surface.blit(self.background, (0, 0))
        self.display_components()


