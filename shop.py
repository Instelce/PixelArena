import pygame
import json


from menu import *
from support import *
from settings import *


class Shop(Menu):
    def __init__(self, menu_type, components, background, create_start_menu) -> None:
        super().__init__(menu_type, components, background)

        self.display_surface = pygame.display.get_surface()

        self.padding_right = 250

        # Card slider
        self.visible_cards = {}
        self.slider_index = 0
        self.slider_arrows = {}

        # Card data
        self.shop_data = read_json_file("data/shop.json")
        self.cards = {}
        self.create_cards()    
        self.create_slider_arrows()

        # Category text
        self.category_texts = []
        self.create_category_text()

        # Back button
        self.back_button = Button("Back", create_start_menu,
                                  (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))

        # Bottom shade
        self.bottom_shade = pygame.transform.scale(pygame.image.load(r"graphics\ui\bottom_shade.png").convert_alpha(), (SCREEN_WIDTH, 100))
        self.bottom_shade_rect = self.bottom_shade.get_rect(bottomleft=(0, SCREEN_HEIGHT))

    def create_category_text(self):
        start_pos = [self.padding_right, 140]
        gap = 300
        for category_place, category in enumerate(self.shop_data):
            if category_place != 0:
                pos = [start_pos[0], (start_pos[1] + gap) * category_place]
            else:
                pos = start_pos
            text = Text('normal', category.upper(), UI_FONT, 40, 'white', pos)
            self.category_texts.append(text)

    def create_cards(self):
        start_pos = [self.padding_right, 180]
        card_size = [200, 240]
        gap = (40, 60)

        for category_place, category in enumerate(self.shop_data):
            print(category, category_place)

            self.cards[category] = []
            self.visible_cards[category] = [0, 1, 2]
            self.slider_arrows[category] = []

            for item_place, item in enumerate(self.shop_data[category]):
                pos = [start_pos[0] + (card_size[0] + gap[0]) * item_place,
                       start_pos[1] + (card_size[1] + gap[1]) * category_place]
                card = Card(pos, item)
                self.cards[category].append(card)

                print(item, item_place)
                print(self.cards)
                print(pos)

    def create_slider_arrows(self):
        left_arrow_start_pos = [200, 200]
        right_arrow_start_pos = [SCREEN_WIDTH-200, 200]
        gap = 300

        for category_place, category in enumerate(self.slider_arrows):
            left_arrow_pos = [left_arrow_start_pos[0], (left_arrow_start_pos[1] + gap) * category_place]
            right_arrow_pos = [right_arrow_start_pos[0], (right_arrow_start_pos[1] + gap) * category_place]
            left_arrow = Button("", None, left_arrow_pos, 60, r"graphics\ui\arrow\default.png", r"graphics\ui\arrow\hover.png")
            right_arrow = Button("", None, right_arrow_pos, 60, r"graphics\ui\arrow\default.png", r"graphics\ui\arrow\hover.png")
            self.slider_arrows[category].append(left_arrow)
            self.slider_arrows[category].append(right_arrow)

    def display_cards(self):
        for category_index, category in enumerate(self.cards):
            for card_index, card in enumerate(self.cards[category]):
                for visible_card in self.visible_cards[category]:
                    if card_index == visible_card:
                        card.display()

    def display_category_text(self):
        for text in self.category_texts:
            text.display()

    def display_slider_arrows(self):
        for category in self.slider_arrows:
            for arrow in self.slider_arrows[category]:
                arrow.display()

    def display(self):
        self.components_reposition()
        self.display_surface.blit(self.background, (0, 0))

        self.display_cards()
        self.display_category_text()
        self.display_slider_arrows()

        self.display_surface.blit(self.bottom_shade, self.bottom_shade_rect)
        self.back_button.display()

        self.display_components()


class Card:
    def __init__(self, pos, data) -> None:
        self.name = data['name']
        self.price = data['price']
        self.category = data['category']
        self.graphics = data['graphics']
        self.stats = data['stats']
        self.pos = pos

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

        # Stats
        self.stats_texts = []
        self.create_stats_text()

    def create_stats_text(self):
        start_pos = [self.pos[0] + 20, self.pos[1] + 160]
        gap = 2
        for stat_place, stat in enumerate(self.stats):
            text = stat.replace('_', ' ').upper()
            pos = [start_pos[0],
                       start_pos[1] + (UI_FONT_SIZE + gap) * stat_place]

            stat_text = Text("normal", f"{text} : {self.stats[stat]}", UI_FONT, UI_FONT_SIZE, "white", pos)
            self.stats_texts.append(stat_text)

    def display_stats(self):
        for text in self.stats_texts:
            text.display()

    def display(self):
        # Draw
        self.display_surface.blit(self.container, self.container_rect)
        self.display_surface.blit(self.graphics_image, self.graphics_rect)
        self.name_text.display()
        self.display_stats()
        self.buy_button.display()
