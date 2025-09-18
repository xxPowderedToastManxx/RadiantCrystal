# from RadiantCrystal import screen

import Globals
import pygame

import json
import sys

# Initialize Pygame
pygame.init()





class UIController:

    def __init__(self):


        self.draw_scroll_background()


    # Function to show the title sequence
    def title_sequence(self):

        

        self.draw_text("Welcome to Your Game", 200, 250)
        self.draw_text("Press any key to start", 250, 300)
       

        new_game_text = self.draw_text("1. New Game", 50, 100)
        self.draw_text("2. Load Game", 50, 150)
        self.draw_text("3. Save Game", 50, 200)  # New option for saving progress
        self.draw_text("4. Quit", 50, 250)  # Adjusted option for quitting the game

        pygame.display.flip()
        # Function to save game progress
        
        menu_choice = None
        while not menu_choice or menu_choice not in ["1", "2", "3", "4"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        menu_choice = "1"
                    elif event.key == pygame.K_2:
                        menu_choice = "2"
                    elif event.key == pygame.K_3:
                        menu_choice = "3"
                    elif event.key == pygame.K_4:
                        menu_choice = "4"

        if menu_choice == "1":
            # New Game
            # Continue with the rest of the game loop
            print("New Game...")

            pass
        elif menu_choice == "2":
            # Load Game
            # ui_controller.load_progress(player, monster, shopkeeper)
            print("Load Game...")
        elif menu_choice == "3":
            # Save Game
            # ui_controller.save_progress(player, monster, shopkeeper)
            print("Save Game...")
        elif menu_choice == "4":
            pygame.quit()
            sys.exit()
        

    def save_progress(self, player, monster, shopkeeper):
        progress = {
            "player": {
                "name": player.name,
                "level": player.level,
                "health": player.health,
                "attack": player.attack,
                "magic_power": player.magic_power,
                "experience": player.experience,
                "money": player.money,
                "inventory": player.inventory.items
            },
            "monster": {
                "name": monster.name,
                "level": monster.level,
                "health": monster.health,
                "attack": monster.attack
            },
            "shopkeeper": {
                "inventory": shopkeeper.inventory.items
            }
        }

        with open("progress.json", "w") as file:
            json.dump(progress, file)

        self.draw_text("Progress saved!", 50, 500)
        pygame.display.flip()
        pygame.time.delay(2000)

    # Function to load game progress
    def load_progress(self, player, monster, shopkeeper):
        try:
            with open("progress.json", "r") as file:
                progress = json.load(file)

            # Update player attributes
            player.name = progress["player"]["name"]
            player.level = progress["player"]["level"]
            player.health = progress["player"]["health"]
            player.attack = progress["player"]["attack"]
            player.magic_power = progress["player"]["magic_power"]
            player.experience = progress["player"]["experience"]
            player.money = progress["player"]["money"]
            player.inventory.items = progress["player"]["inventory"]

            # Update monster attributes
            monster.name = progress["monster"]["name"]
            monster.level = progress["monster"]["level"]
            monster.health = progress["monster"]["health"]
            monster.attack = progress["monster"]["attack"]

            # Update shopkeeper's inventory
            shopkeeper.inventory.items = progress["shopkeeper"]["inventory"]

            self.draw_text("Progress loaded!", 50, 500)
            pygame.display.flip()
            pygame.time.delay(2000)

        except FileNotFoundError:
            self.draw_text("No saved progress found.", 50, 500)
            pygame.display.flip()
            pygame.time.delay(2000)


    # Function to display text on the screen
    def draw_text(self, text, x, y):
        surface = Globals.FONT.render(text, True, Globals.BLACK)
        Globals.screen.blit(surface, (x, y))

    # Function to create scrolling text animation
    def scroll_text_animation(self, lines):
        y_position = Globals.HEIGHT + 50

        for line in lines:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))  # Clear the screen
            self.draw_scroll_background()
            self.draw_text(line, 50, y_position)
            y_position -= 30

            pygame.display.flip()
            pygame.time.delay(1000)  # Adjust the delay to control the scrolling speed

    # Function to draw a scroll-like background
    def draw_scroll_background(self):
        pygame.draw.rect(Globals.screen, (204, 175, 118), (25, 25, Globals.WIDTH - 50, Globals.HEIGHT - 50), border_radius = 10)

    # Function to draw UI with available options
    def draw_ui(self,options):
        
        for i, option in enumerate(options, start=1):
            pygame.draw.rect(self.screen, self.WHITE, (50, 50 + i * 50, self.WIDTH - 100, 40), 2)
            self.draw_text(option, 60, 60 + i * 50)

    def new_game(self):
        return


    def delete(self, obj):

        return