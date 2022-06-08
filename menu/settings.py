import pygame

from menu.default import Menu
from menu.components import *


class Settings(Menu):
    def __init__(self, menu_type, components, background) -> None:
        super().__init__(menu_type, components, background)