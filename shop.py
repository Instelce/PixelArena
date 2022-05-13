import pygame
import json


from menu import *
from support import *


class Shop(Menu):
    def __init__(self, menu_type, components, background, create_start_menu) -> None:
        super().__init__(menu_type, components, background)

        self.display_surface = pygame.display.get_surface()

        # Card data
        self.shop_data = read_json_file("data/shop.json")
        print(self.shop_data)
        self.cards = []

        # Back button
        self.back_button = Button("Back", create_start_menu,
                                  (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))

        self.add_cards()

    def add_cards(self):
        start_pos = [250, 180]
        card_size = [200, 240]
        gap = 40

        for category_place, category in enumerate(self.shop_data):
            print(category, category_place)
            for item_place, item in enumerate(self.shop_data[category]):
                pos = [start_pos[0] + (card_size[0] + gap) * item_place,
                       start_pos[1] + (card_size[1] + gap) * category_place]
                card = Card(pos, item)
                self.cards.append(card)
                print(item, item_place)
                print(self.cards)
                print(pos)

    def display_cards(self):
        for card in self.cards:
            card.display()

    def display(self):
        self.components_reposition()
        self.display_surface.blit(self.background, (0, 0))
        self.display_cards()
        self.back_button.display()

        self.display_components()


class Card:
    def __init__(self, pos, data) -> None:
        self.name = data['name']
        self.price = data['price']
        self.category = data['category']
        self.graphics = data['graphics']
        self.stats = data['stats']

        self.display_surface = pygame.display.get_surface()

        # Container
        self.container = pygame.image.load(
            "graphics/ui/card/container.png").convert_alpha()
        self.container_rect = self.container.get_rect(topleft=pos)
        self.size = self.container.get_size()

        # Image
        self.graphics_image = pygame.image.load(self.graphics).convert_alpha()
        self.graphics_rect = self.graphics_image.get_rect(
            center=[pos[0] + 100, pos[1] + 60])

        # Name
        self.name_text = Text("normal", self.name, UI_FONT, 30, 'white',
                              [pos[0] + 20, pos[1] + self.size[1] / 2])

        # Button (BUY)
        self.buy_button = Button(
            "Buy",
            None,
            [pos[0] + (self.size[0] / 2) + 25, pos[1] +
             (self.size[1] - 30) - 3],
            40,
            "graphics/ui/card/button/default.png",
            "graphics/ui/card/button/hover.png")

    def display(self):
        # Draw
        self.display_surface.blit(self.container, self.container_rect)
        self.display_surface.blit(self.graphics_image, self.graphics_rect)
        self.name_text.display()
        self.buy_button.display()
