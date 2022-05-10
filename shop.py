import pygame


from menu import *
from support import import_json_data


class Shop(Menu):
    def __init__(self, menu_type, components, background) -> None:
        super().__init__(menu_type, components, background)

        self.display_surface = pygame.display.get_surface()

        # Card data
        self.shop_data = import_json_data("data/shop.json")
        print(self.shop_data)
        self.cards = []

    def display(self):
        self.components_reposition()
        self.display_surface.blit(self.background, (0, 0))

        self.display_components()


class Card:
    def __init__(self, data) -> None:
        self.name = data['name']
        self.price = data['price']
        self.category = data['category']
        self.graphics = data['graphics']
        self.stats = data['stats']
        self.size = [200, 150]

        self.display_surface = pygame.display.get_surface()

        self.bg_rect = bg_rect = pygame.Rect(
            20, 20, self.size[0], self.size[1])

    def display(self):
        # Draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.bg_rect)
