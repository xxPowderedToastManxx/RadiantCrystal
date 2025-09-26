import sys
import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel

from .base_app_state import BaseAppState
from ui_adapter import UIAdapter
from .combat_state import CombatState
from Player import Player
from monster_factory import random_monster





class MainMenu(BaseAppState):

    def __init__(self, screen_data, ui_manager: pygame_gui.UIManager, state_manger):
        super().__init__('main_menu', 'game', state_manger)

        self.screen_data = screen_data
        self.ui_manager = ui_manager
        self.background_image = pygame.image.load("images/title.jpeg").convert()

        

        self.new_game_button = None
        self.load_game_button = None

        print(screen_data.screen_size)

        
    def start(self):
        
        self.new_game_button = UIButton(pygame.Rect((350, 515), (150, 35)),
                                         "New Game", self.ui_manager,
                                         tool_tip_text="<b>Click to Start.</b>")


        self.load_game_button = UIButton(pygame.Rect((550, 515), (150, 35)),
                                    "Load Game", self.ui_manager,
                                    tool_tip_text="<b>Click to Start.</b>")
        print("MainMenu: created New Game and Load Game buttons")

    def end(self):

        self.new_game_button.kill()
        self.load_game_button.kill()

    def run(self, surface, time_delta):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.set_target_state_name('quit')
                self.trigger_transition()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_target_state_name('quit')
                    self.trigger_transition()

                if event.key == pygame.K_w:
                    print("W key pressed...")

                
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.new_game_button:
                    # Create a UI adapter tied to this ui_manager and register a CombatState
                    ui_adapter = UIAdapter(None, None, self.ui_manager)
                    # create simple player and monster instances and pass them to the new state
                    player = Player("Hero")
                    monster = random_monster()
                    print(f"MainMenu: New Game pressed, spawning monster {monster.name}")

                    combat_state = CombatState(ui_adapter, self.state_manager)
                    # provide incoming data so the combat state can use real objects
                    combat_state.incoming_transition_data = {"player": player, "monster": monster}

                    self.set_target_state_name('combat')
                    self.trigger_transition()
                    # print("New Game Button Pushed...")

            #     elif event.ui_element == self.load_game_button:
            #         self.set_target_state_name('load_state')
            #         self.trigger_transition()
            #         print("Load Game Button Pushed...")




            

            self.ui_manager.process_events(event)

        self.ui_manager.update(time_delta)

        surface.blit(self.background_image, (0, 0))  # draw the background

        self.ui_manager.draw_ui(surface)
