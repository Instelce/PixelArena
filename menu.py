import pygame
from math import floor

from settings import *


class Menu:
    def __init__(self, menu_type, title, components, background) -> None:
        self.menu_type = menu_type
        self.title = title
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
                    component_size = list(component.size)
                    print(start_pos, component_pos, component_size)
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


class Button:
    def __init__(self, text, callback, pos, default_image="graphics/ui/buttons/button_large_default.png", hover_image="graphics/ui/buttons/button_large_hover.png", margin=60) -> None:
        self.text = text
        self.callback = callback
        self.pos = pos
        self.margin = margin

        self.display_surface = pygame.display.get_surface()

        # Image
        self.default_image = default_image
        self.hover_image = hover_image
        self.image = pygame.image.load(self.default_image).convert_alpha()
        self.size = self.image.get_size()

    def check_hover_click(self):
        mouse_pos = pygame.mouse.get_pos()

        # Hover
        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.image.load(self.hover_image).convert_alpha()

            self.display_surface.blit(self.image, self.rect)

            # Click
            if pygame.mouse.get_pressed()[0]:
                if self.callback != None:
                    self.callback()
        else:
            self.image = pygame.image.load(self.default_image).convert_alpha()
            self.display_surface.blit(self.image, self.rect)

    def display_text(self):
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        text_surf = font.render(self.text, False, "black")
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.display_surface.blit(text_surf, text_rect)

    def display(self):
        if self.pos != None:
            self.rect = self.image.get_rect(midtop=self.pos)
        self.check_hover_click()
        self.display_text()


class Text:
    def __init__(self, text, font, font_size, color, pos, margin=40):
        self.text = text
        self.margin = margin
        self.pos = pos

        self.display_surface = pygame.display.get_surface()

        # Text
        self.font = pygame.font.Font(font, font_size)
        self.text_surf = self.font.render(str(text), False, color)
        self.text_rect = self.text_surf.get_rect(midtop=pos)
        self.size = font_size

    def display(self):
        self.display_surface.blit(self.text_surf, self.text_rect)
