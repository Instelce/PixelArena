import string
import pygame
from math import floor
from random import randint

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

                    print('increase')
                    print('size', self.size)

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

                print("dicrease")
                print('size', self.size)

                if self.size <= 0:
                    self.size = 0
                    self.transition_is_finish = True

            pygame.draw.rect(self.display_surface, 'black', pygame.Rect(SCREEN_WIDTH-self.size, 0, self.size, SCREEN_HEIGHT))
            
            if self.size >= SCREEN_WIDTH/2:
                self.loading_text.display()


class LoadingBar:
    def __init__(self, tasks, redirect) -> None:
        self.tasks = tasks
        self.pos = (SCREEN_WIDTH/2, 0)
        self.margin = 60
        self.display_surface = pygame.display.get_surface()
        self.last_time = pygame.time.get_ticks()
        self.redirect = redirect

        self.border = pygame.image.load(r"graphics\ui\loadingbar\border.png")
        self.rect = self.border.get_rect(midtop=self.pos)
        self.size = self.border.get_size()

        self.original_fill = pygame.image.load(r"graphics\ui\loadingbar\fill.png").convert_alpha()
        self.task_text = Text('center', "", UI_FONT, UI_FONT_SIZE, 'white', self.border.get_rect().center)
        self.bar_width = 0

        self.task_index = 0
        self.last_task_index = self.task_index
    
    def load(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_time >= randint(100, 400) and self.task_index < len(self.tasks)-1 and self.last_task_index == self.task_index:
            self.last_time = current_time
            self.task_index += 1

        self.fill_image = pygame.transform.scale(self.original_fill, (self.bar_width, self.size[1] - 12))
        self.fill_rect = self.fill_image.get_rect(topleft=(self.pos[0]-self.size[0]/2 + 6, self.pos[1] + 6))

        self.task_text = Text('center', self.tasks[self.task_index], UI_FONT, UI_FONT_SIZE, 'white', (self.rect.centerx, self.rect.centery - 6))
        
        if self.last_task_index != self.task_index:
            current_ratio = self.task_index / len(self.tasks)
            last_ratio = self.last_task_index / len(self.tasks)
            part_size = self.size[0] / len(self.tasks)
            current_width = floor(self.size[0] * current_ratio)
            last_width = floor(self.size[0] * last_ratio)

            if self.bar_width <= current_width:
                if current_time - self.last_time >= 5:
                    self.last_time = current_time
                    self.bar_width += 1
            if self.bar_width == current_width:
                self.last_task_index = self.task_index

            print("INDEX CHANGE ---------------")
            print(self.last_task_index, '/', self.task_index, '/', len(self.tasks))
            print("size :", self.fill_rect.width)
            print("current :", current_width, current_ratio)
            print("last :", last_width, last_ratio)
            print("tasks :", self.tasks[self.task_index])
        
        if self.task_index == len(self.tasks) - 1:
            self.bar_width = 0
            self.task_index = 0
            self.last_task_index = 0

            self.redirect()

        self.display_surface.blit(self.fill_image, self.fill_rect)
        self.task_text.display()
    
    def display(self):
        self.load()
        self.rect = self.border.get_rect(midtop=self.pos)
        self.display_surface.blit(self.border, self.rect)
        
        
class Button:
    def __init__(self, content, callback=None, pos=None, margin=60, default_image="graphics/ui/buttons/button_large_default.png", hover_image="graphics/ui/buttons/button_large_hover.png") -> None:
        self.content = content
        self.callback = callback
        self.pos = (SCREEN_WIDTH/2, 200) if pos is None else pos
        self.margin = margin

        self.display_surface = pygame.display.get_surface()
        self.click = False

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
                self.click = True
                if self.callback != None:
                    self.callback()
            else:
                self.click = False
        else:
            self.image = pygame.image.load(self.default_image).convert_alpha()
            self.display_surface.blit(self.image, self.rect)

    def display_text_or_image(self):
        if '/' in self.content or "\\" in self.content:
            # Image
            image = pygame.image.load(self.content).convert_alpha()
            image_rect = image.get_rect(center=self.rect.center)
            self.display_surface.blit(image, image_rect)
        else:
            # Text
            font = pygame.font.Font(UI_FONT, BUTTON_FONT_SIZE)
            text_surf = font.render(self.content, False, "black")
            text_rect = text_surf.get_rect(center=self.rect.center)
            self.display_surface.blit(text_surf, text_rect)

    def display(self):
        self.rect = self.image.get_rect(midtop=self.pos)
        self.check_hover_click()
        self.display_text_or_image()


class Text:
    def __init__(self, alignement, text, font=UI_FONT, font_size=UI_FONT_SIZE, color='white', pos=None, margin=60):
        self.alignement = alignement
        self.text = text
        self.margin = margin
        self.pos = (SCREEN_WIDTH/2, 0) if pos is None else pos

        self.display_surface = pygame.display.get_surface()

        # Text
        self.font = pygame.font.Font(font, font_size)
        self.text_surf = self.font.render(str(text), False, color)
        if self.alignement == 'center':
            self.rect = self.text_surf.get_rect(midtop=self.pos)
            # self.rect = self.text_surf.get_rect(center=self.pos)
        else:
            self.rect = self.text_surf.get_rect(topleft=self.pos)
        self.size = (font_size, font_size)

    def display(self):
        if self.alignement == 'center':
            self.rect = self.text_surf.get_rect(midtop=self.pos)
        else:
            self.rect = self.text_surf.get_rect(topleft=self.pos)
        self.display_surface.blit(self.text_surf, self.rect)


class Input:
    def __init__(self, placeholder=None, font=UI_FONT, font_size=UI_FONT_SIZE, color='black', pos=None, margin=None) -> None:
        self.value = ''
        self.placeholder = 'Input' if placeholder is None else placeholder

        self.display_surface = pygame.display.get_surface()
        self.pos = (SCREEN_WIDTH/2, 0) if pos is None else pos
        self.margin = 60 if margin is None else margin
        self.size = (200, font_size + 20)
        self.font = pygame.font.SysFont('calibri', font_size)
        self.font_size = font_size
        self.color = color

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.cursor = pygame.Rect(self.pos[0] + len(self.value) * 5, self.pos[1], 2, font_size)

        self.last_time = pygame.time.get_ticks()
        self.key_cooldown = 150

        self.focus = False

        self.get_input()

    def get_input(self):
        self.letters = list(string.printable)
        self.special_caracters = "&é\"'(-è_çà"
        self.number_caracters = "1234567890"
        self.keys_keycode = {}

        for letter in self.letters:
            self.keys_keycode[letter] = pygame.key.key_code(letter)
    
    def check_focus(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.focus = True
                self.color = 'white'
        else:
            if pygame.mouse.get_pressed()[0]:
                self.focus = False
                self.color = "black"

    def get_key_pressed(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.focus:
            for keycode in self.keys_keycode:
                if keys[self.keys_keycode[keycode]] and current_time - self.last_time >= self.key_cooldown:
                    self.last_time = current_time
                    if 49 <= self.keys_keycode[keycode] <= 61:
                        if keys[pygame.K_LSHIFT]:
                            self.value += pygame.key.name(self.keys_keycode[keycode])
                        else:
                            index = abs(61-(int(keycode)+61))-1
                            print("INDEX", index)
                            self.value += self.special_caracters[index]
                    elif keys[pygame.K_LSHIFT]:
                        self.value += pygame.key.name(self.keys_keycode[keycode]).upper()
                    else:
                        self.value += pygame.key.name(self.keys_keycode[keycode])
                            
            if keys[pygame.K_BACKSPACE] and current_time - self.last_time >= self.key_cooldown:
                self.last_time = current_time
                self.value = self.value[:-1]
            if keys[pygame.K_SPACE] and current_time - self.last_time >= self.key_cooldown:
                self.last_time = current_time
                self.value += ' '

            # print(self.value)

    def display(self):
        self.check_focus()

        if self.value != '':
            input_surface = self.font.render(self.value, True, self.color)
        else:
            input_surface = self.font.render(self.placeholder, True, self.color)
        text_input_size = input_surface.get_size()
        input_center = (self.rect.x + self.size[0] / 2 - text_input_size[0]/2, self.rect.y + self.size[1] / 2 - text_input_size[1]/2)
        self.rect = pygame.Rect(self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2, self.size[0], self.size[1])
        
        if text_input_size[0] <= self.size[0] - 20:
            self.get_key_pressed()


        pygame.draw.rect(self.display_surface, self.color, self.rect, 2)
        self.display_surface.blit(input_surface, input_center)

        if self.focus and self.value != '':
            self.cursor = pygame.Rect(input_center[0] + text_input_size[0], input_center[1], 1, self.font_size)
            pygame.draw.rect(self.display_surface, self.color, self.cursor, 2)