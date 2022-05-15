from debug import debug
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
        self.last_time = pygame.time.get_ticks()

        # Card slider
        self.visible_cards = {}
        self.slider_index = 0
        self.slider_arrows = []

        # Card data
        self.shop_data = read_json_file("data/shop.json")
        self.cards = {}
        self.create_cards()
        self.create_slider_arrows()

        # Category text
        self.active_category = 'weapons'
        self.create_category_text()

        # Category buttons
        self.category_buttons = {}
        self.create_category_buttons()

        # Back button
        self.back_button = Button("Back", create_start_menu,
                                  (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))

        # Bottom shade
        self.bottom_shade = pygame.transform.scale(pygame.image.load(
            r"graphics\ui\bottom_shade.png").convert_alpha(), (SCREEN_WIDTH, 100))
        self.bottom_shade_rect = self.bottom_shade.get_rect(
            bottomleft=(0, SCREEN_HEIGHT))

    def create_category_text(self):
        pos = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 180]
        self.category_text = Text('title', self.active_category.upper(), UI_FONT, 40, 'white', pos)

    def create_cards(self):
        card_size = [200, 240]
        gap = 40
        start_pos = [SCREEN_WIDTH/2 - (card_size[0]/2 + card_size[0] + gap), SCREEN_HEIGHT/2 - card_size[1]/2]

        for category_place, category in enumerate(self.shop_data):
            print(category, category_place)

            self.cards[category] = []
            self.visible_cards[category] = [0, 1, 2]

            for item_place, item in enumerate(self.shop_data[category]):
                pos = [start_pos[0] + (card_size[0] + gap) * item_place,
                       start_pos[1]]
                card = Card(pos, item)
                self.cards[category].append(card)

                print(item, item_place)
                print(self.cards)
                print(pos)

    def create_category_buttons(self):
        button_size = 50
        gap = 10
        start_pos = [SCREEN_WIDTH/2 - len(self.shop_data)/2 * (button_size), SCREEN_HEIGHT/2 + 180]
        print(start_pos)
        for category_place, category in enumerate(self.shop_data):
            pos = [start_pos[0] + (button_size + gap) * category_place, start_pos[1]]
            self.category_buttons[category] = Button(f"graphics/ui/categories/{category}.png", None, pos, 60, 
            "graphics/ui/buttons/category/default.png",
            "graphics/ui/buttons/category/hover.png")

    def create_slider_arrows(self):
        left_arrow_pos = [180, SCREEN_HEIGHT / 2 - 50]
        right_arrow_pos = [SCREEN_WIDTH - 180, SCREEN_HEIGHT / 2 - 50]

        left_arrow = Button("", None, left_arrow_pos, 60,
                            r"graphics\ui\arrow\left\default.png", r"graphics\ui\arrow\left\hover.png")
        right_arrow = Button("", None, right_arrow_pos, 60,
                                r"graphics\ui\arrow\right\default.png", r"graphics\ui\arrow\right\hover.png")

        self.slider_arrows.append(left_arrow)
        self.slider_arrows.append(right_arrow)

    def slide(self):
        current_time = pygame.time.get_ticks()

        for category in self.cards:
            for arrow_index, arrow in enumerate(self.slider_arrows):
                if arrow.click:
                    if current_time - self.last_time >= 200:
                        self.last_time = current_time
                        print(f"ARROW CLICK {category} {arrow_index}")
                        print(self.visible_cards[category], len(self.shop_data[category]) - 1)

                        if arrow_index == 0:
                            print("LEFT")
                            if self.visible_cards[category][0] != 0:
                                self.visible_cards[category].remove(self.visible_cards[category][-1])
                                self.visible_cards[category].insert(0, self.visible_cards[category][0] - 1)
                                self.visible_cards[category].sort()
                        elif arrow_index == 1:
                            print("RIGHT")
                            if self.visible_cards[category][-1] < len(self.shop_data[category]) - 1:
                                self.visible_cards[category].remove(self.visible_cards[category][0])
                                self.visible_cards[category].append(self.visible_cards[category][-1] + 1)
                                self.visible_cards[category].sort()
    
    def change_category(self):
        for category in self.category_buttons:
            button = self.category_buttons[category]

            if button.click:
                self.active_category = category
                self.create_category_text()

    def display_cards(self):
        card_size = [200, 240]
        gap = 40
        start_pos = [SCREEN_WIDTH/2 - (card_size[0]/2 + card_size[0] + gap), SCREEN_HEIGHT/2 - card_size[1]/2]

        for category_index, category in enumerate(self.cards):
            for card_index, card in enumerate(self.cards[category]):
                for visible_card_index, visible_card in enumerate(self.visible_cards[category]):
                    if card_index == visible_card and category == self.active_category:
                        card.pos = [start_pos[0] + (card_size[0] + gap) * visible_card_index, start_pos[1]]
                        card.display()
                    if card.data_is_update:
                        self.shop_data = read_json_file("data/shop.json")
                        self.create_cards()

    def display_slider_arrows(self):
        # if self.visible_cards[self.active_category][0] == 0:
        #     self.slider_arrows[1].image.set_alpha(0)
        # else:
        #     self.slider_arrows[1].image.set_alpha(255)
        # if self.visible_cards[self.active_category][-1] == len(self.shop_data[self.active_category]) - 1:
        #     self.slider_arrows[0].image.set_alpha(0)
        # else:
        #     self.slider_arrows[0].image.set_alpha(255)
            
        for category in self.cards:
            for arrow_index, arrow in enumerate(self.slider_arrows):
                if len(self.cards[category]) > 3:
                    arrow.display()

    def display_category_buttons(self):
        for category in self.category_buttons:
            self.category_buttons[category].display()

    def display(self):
        self.components_reposition()
        self.display_surface.blit(self.background, (0, 0))

        self.display_cards()
        self.display_slider_arrows()
        self.display_category_buttons()

        self.category_text.display()
        self.display_surface.blit(self.bottom_shade, self.bottom_shade_rect)
        self.back_button.display()

        self.display_components()
        
        self.change_category()
        self.slide()

        debug(self.visible_cards[self.active_category], 20)


class Card:
    def __init__(self, pos, data) -> None:
        self.data = data
        self.name = data['name']
        self.price = data['price']
        self.category = data['category']
        self.graphics = data['graphics']
        self.stats = data['stats']
        self.pos = pos

        self.display_surface = pygame.display.get_surface()

        # Background
        self.background = pygame.image.load(
            "graphics/ui/card/container.png").convert_alpha()
        self.background_rect = self.background.get_rect(topleft=pos)
        self.size = self.background.get_size()

        # Image
        self.graphics_image = pygame.image.load(self.graphics).convert_alpha()
        self.graphics_rect = self.graphics_image.get_rect(
            center=[pos[0] + 100, pos[1] + 60])

        # Name
        self.name_text = Text("normal", self.name, UI_FONT, 30, 'white',
                              [pos[0] + 20, pos[1] + self.size[1] / 2])

        # Buy button
        self.buy_button = Button(
            "",
            self.update_inventory_shop_data,
            [pos[0] + (self.size[0] / 2) + 25, pos[1] +
             (self.size[1] - 30) - 3],
            40,
            "graphics/ui/card/button/default.png",
            "graphics/ui/card/button/hover.png")
        self.price_text = Text('normal', self.price, UI_FONT, UI_FONT_SIZE, 'white', 
        [pos[0] + 22, pos[1] + 214])

        # Stats
        self.stats_texts = []
        self.create_stats_text()

        # Data
        self.data_is_update = False

    def update_inventory_shop_data(self):
        if not self.data_is_update:
            # Update inventory
            inventory_data = read_json_file("data/inventory.json")
            inventory_data[self.category].append(self.data)
            write_json_file("data/inventory.json", {})
            write_json_file("data/inventory.json", inventory_data)

            # Update shop
            shop_data = read_json_file("data/shop.json")
            print(shop_data[self.category])
            shop_data[self.category].remove(self.data)
            write_json_file("data/shop.json", {})
            write_json_file("data/shop.json", shop_data)
            
            self.data_is_update = True

    def create_stats_text(self):
        self.stats_texts = []

        start_pos = [self.pos[0] + 20, self.pos[1] + 160]
        gap = 2

        for stat_place, stat in enumerate(self.stats):
            text = stat.replace('_', ' ').upper()
            pos = [start_pos[0],
                   start_pos[1] + (UI_FONT_SIZE + gap) * stat_place]

            stat_text = Text(
                "normal", f"{text} : {self.stats[stat]}", UI_FONT, UI_FONT_SIZE, "white", pos)
            self.stats_texts.append(stat_text)
    
    def update_rect(self):
        # Background
        self.background_rect = self.background.get_rect(topleft=self.pos)

        # Image
        self.graphics_rect = self.graphics_image.get_rect(
            center=[self.pos[0] + 100, self.pos[1] + 60])

        # Name
        self.name_text = Text("normal", self.name, UI_FONT, 30, 'white',
                              [self.pos[0] + 20, self.pos[1] + self.size[1] / 2])
        
        # Stats
        self.create_stats_text()

        # Buy button
        self.buy_button = Button(
            "",
            self.update_inventory_shop_data,
            [self.pos[0] + (self.size[0] / 2) + 25, self.pos[1] +
             (self.size[1] - 30) - 3],
            40,
            "graphics/ui/card/button/default.png",
            "graphics/ui/card/button/hover.png")
        self.price_text = Text('normal', self.price, UI_FONT, UI_FONT_SIZE, 'white', 
        [self.pos[0] + 22, self.pos[1] + 214])

    def display_stats(self):
        for text in self.stats_texts:
            text.display()

    def display(self):
        # Update
        self.update_rect()

        # Draw
        self.display_surface.blit(self.background, self.background_rect)
        self.display_surface.blit(self.graphics_image, self.graphics_rect)
        self.name_text.display()
        self.display_stats()
        self.buy_button.display()
        self.price_text.display()
