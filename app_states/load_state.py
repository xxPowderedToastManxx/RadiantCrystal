import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel

from .base_app_state import BaseAppState


from Player import Player


class LoadState(BaseAppState):
    def __init__(self, ui_manager: pygame_gui.UIManager, state_manger):
        super().__init__('load_state', 'game', state_manger)

        self.ui_manager = ui_manager
        
        
 