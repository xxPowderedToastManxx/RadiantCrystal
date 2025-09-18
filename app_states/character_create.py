import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel

import Globals

from .base_app_state import BaseAppState


from Player import Player


class CharacterCreate(BaseAppState):
    def __init__(self, screen_data, ui_manager: pygame_gui.UIManager, state_manger):
        super().__init__('character_create', 'game', state_manger)

        self.background_image = pygame.image.load("images/title.jpeg").convert() # Change to new background, ancient scroll like look

        self.ui_manager = ui_manager
        # print("CharacterCreate Initalized...")
        self.race_choice = Globals.RACES
        

    def start(self):
        
        self.new_game_button = UIButton(pygame.Rect((350, 515), (150, 35)),
                                         "Race", self.ui_manager,
                                         tool_tip_text="<b>Click to Start.</b>")


        self.load_game_button = UIButton(pygame.Rect((550, 515), (150, 35)),
                                    "Class", self.ui_manager,
                                    tool_tip_text="<b>Click to Start.</b>")

    def end(self):
        # self.title_label.kill()
        self.new_game_button.kill()
        self.load_game_button.kill()

    def run(self, surface, time_delta):
        pass