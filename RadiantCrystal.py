import os

import pygame
# from pygame.locals import *

import sys
import random
# import json

import Player
import Inventory
import Shopkeeper
import Monster

import Globals

import Timeline

from pygame_gui import UIManager 
from DiceController import DiceController


# Remove UIController script and use state manager to control UI elements
# There needs to be a transition between states, some kind of animation
# Add in DialogManager and the data structures for dialog, dialog needs to load from json, research
# Need to addin proficiency bonus rolls and assignments
# get D&D books from upstairs
# Add in scrolling animation for panels opening up
# Add in buttons (pygame_gui)
# Add in touch, controller and mouse/keyboard input in EventHandeler script
# Add in CombatTester script to easily test combat
# Add an AnimationController script to handle animations of panels and buttons
# Inventory panel with buttons on a grid, another panel shows item and its attributes
# Don't forget to employ pygame groups to manage sprites (buttons)
# Aquire artwork for navigation, avatars, weapons, armour, items, magical shit
# Add magic spells and the implementation of using them
# Update ui_theme.json file to include all new buttons and panels
# Create a "scroll" looking panel and button backgrounds
# Create Dialog panels and figure out how to place them on the screen in the desired location
# Add in saving and loading gamestates
# Add in shopping/selling state
# Add in equipping and unequipping items
# Create settings state to manipulate in-game settings
# Create a flowchart of gamestates and gameplay

# How does state manager switch states with the "name"



# Game States to add
# New Game State - Create Class/Race - Start Game
# Save Game State - Only available from game state menu
# Load Game State - Available from Title Screen and 

# Import states

from app_states.app_state_manager import AppStateManager
from app_states.main_menu import MainMenu
from app_states.character_create import CharacterCreate

from app_states.load_state import LoadState
# from game.app_states.editor_state import EditorState
from app_states.quit_state import QuitState

# Initialize Pygame
# pygame.init()


# # Constants
# WIDTH, HEIGHT = 800, 600
# FPS = 30
# WHITE = (255, 255, 255)
# FONT = pygame.font.Font(None, 36)

# global player_health, player_experience

# Game variables
# player_name = "Hero"
# player_level = 1
# player_health = 100
# player_attack = 20
# player_experience = 0

# Monster variables
# monster_names = ["Goblin", "Skeleton", "Orc"]
# monster_levels = [1, 2, 3]
# monster_healths = [30, 50, 80]
# monster_attacks = [15, 25, 35]

# ui_controller = UIController()
dice = DiceController()


# Add pygame_gui, and state manager classes to handle states of gameplay

class ScreenData:
    # def __init__(self, hud_size, screen_size):
    def __init__(self, screen_size):

        self.screen_size = screen_size

    #     self.hud_dimensions = hud_size

    #     self.play_area = [screen_size[0], screen_size[1] - self.hud_dimensions[1]]

    # def set_editor_active(self):
    #     self.play_area = [self.screen_size[0], self.screen_size[1] - self.editor_hud_dimensions[1]]

    # def set_editor_inactive(self):
    #     self.play_area = [self.screen_size[0], self.screen_size[1] - self.hud_dimensions[1]]


def main():
    # pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.key.set_repeat()
    # x_screen_size = Globals.WIDTH
    # y_screen_size = Globals.HEIGHT
    
    # screen = pygame.display.set_mode((x_screen_size, y_screen_size))

    # screen_data = ScreenData([x_screen_size, 128], [x_screen_size, y_screen_size])
    screen_data = ScreenData([Globals.WIDTH, Globals.HEIGHT])

    ui_manager = UIManager(Globals.SCREEN.get_size(), "data/ui_theme.json")
    ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                              {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                              {'name': 'fira_code', 'point_size': 12, 'style': 'bold'}])

    app_state_manager = AppStateManager()
    MainMenu(screen_data, ui_manager, app_state_manager)
    LoadState(ui_manager, app_state_manager)
    CharacterCreate(screen_data, ui_manager, app_state_manager)

    # GameState(ui_manager, screen, screen_data, app_state_manager)

    QuitState(app_state_manager)
    app_state_manager.set_initial_state('main_menu')

    clock = pygame.time.Clock()
    running = True

    while running:
        frame_time = clock.tick(60)
        time_delta = min(frame_time/1000.0, 0.1)

        running = app_state_manager.run(Globals.SCREEN, time_delta)

        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()