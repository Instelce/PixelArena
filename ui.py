import pygame
from settings import *


class UI:
    def __init__(self) -> None:

        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.wave_duration_bar_rect = pygame.Rect(
            SCREEN_WIDTH-(WAVE_DURATION_BAR_WIDTH+10), 10, WAVE_DURATION_BAR_WIDTH, BAR_HEIGHT)

        # Convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            weapon = pygame.image.load(weapon['graphic']).convert_alpha()
            self.weapon_graphics.append(weapon)

        # Convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color, separator_gap=None):
        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Create separators
        separators = []
        sep_count = 0
        if separator_gap != None:
            for i in range(0, max_amount, separator_gap):
                ratio = (sep_count * separator_gap) / max_amount
                pos = bg_rect.width * ratio
                sep_count += 1
                print('Ratio', ratio)
                print('Count', sep_count)
                print('Pos', pos)

                separator = pygame.Rect(bg_rect.left + pos, bg_rect.top, 2, bg_rect.height)
                separators.append(separator)
                
        # Drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        # Drawing separators
        for separator in separators:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, separator)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 16))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 16), 3)
    
    def show_wave_difficulty(self, difficulty):
        text_surf = self.font.render(f"Wave {str(int(difficulty))}", False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 10
        y = 34
        text_rect = text_surf.get_rect(topright=(x, y))

        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        if has_switched:
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, self.display_surface.get_size()[
                                     1] - (ITEM_BOX_SIZE + 20), has_switched)  # Weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(85, self.display_surface.get_size()[
                                     1] - (ITEM_BOX_SIZE + 15), has_switched)  # Magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def inventory_overlay(self):
        pass

    def display(self, player, wave):
        self.show_bar(
            player.health, 
            player.stats['health'], 
            self.health_bar_rect, 
            HEALTH_COLOR)
        self.show_bar(
            player.energy, 
            player.stats['energy'], 
            self.energy_bar_rect, 
            ENERGY_COLOR)
        self.show_bar(
            wave.current_time,
            wave.duration,
            self.wave_duration_bar_rect, 
            WAVE_DURATION_COLOR,
            wave.spawn_cooldown)

        self.show_exp(player.exp)
        self.show_wave_difficulty(wave.difficulty)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
