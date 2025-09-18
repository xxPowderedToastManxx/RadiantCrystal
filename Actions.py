import pygame
import sys
import random

import UIController as ui_controller

class Actions:

    # Function to handle navigation
    def navigate(player, direction):
        if direction == "north":
            ui_controller.draw_text("You move north.", 50, 300)
        elif direction == "south":
            ui_controller.draw_text("You move south.", 50, 300)
        elif direction == "east":
            ui_controller.draw_text("You move east.", 50, 300)
        elif direction == "west":
            ui_controller.draw_text("You move west.", 50, 300)
        else:
            ui_controller.draw_text("Invalid direction.", 50, 300)

    def death_scene():
        ui_controller.draw_text("You have fallen in battle...", 50, 300)
        ui_controller.draw_text("1. Start a New Game", 50, 350)
        ui_controller.draw_text("2. Quit", 50, 400)
        pygame.display.flip()

        choice = None
        while not choice or choice not in ["1", "2"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_2:
                        choice = pygame.key.name(event.key)

        if choice == "1":
            return True  # Start a new game
        elif choice == "2":
            pygame.quit()
            sys.exit()  # Quit the game

# Function to handle environment interactions
    def interact_environment(player, action):
        if action == "search":
            ui_controller.draw_text("You search the area for clues.", 50, 300)
        elif action == "rest":
            ui_controller.draw_text("You take a moment to rest and recover.", 50, 300)
            player.health += 10
        else:
            ui_controller.draw_text("Invalid action.", 50, 300)

    # Function to handle combat
    def combat(player, monster):
        ui_controller.draw_text(f"You encounter a {monster.name} (Level {monster.level})!", 50, 300)
        pygame.display.flip()
        pygame.time.delay(1000)

        while player.health > 0 and monster.health > 0:
            # Player's turn
            ui_controller.draw_text("1. Melee Attack", 50, 100)
            ui_controller.draw_text("2. Magic Attack", 50, 150)
            ui_controller.draw_text("3. Use Item", 50, 200)
            pygame.display.flip()

            player_action = None
            while action not in ["1", "2", "3"]:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            action = "1"
                        elif event.key == pygame.K_2:
                            action = "2"
                        elif event.key == pygame.K_3:
                            action = "3"

            if action == "1":
                # Melee Attack
                damage = random.randint(player.attack - 5, player.attack + 5)
                monster.take_damage(damage)
                ui_controller.draw_text(f"You deal {damage} damage with a melee attack!", 50, 300)
            elif action == "2":
                # Magic Attack
                if player.magic_power >= 10:
                    damage = random.randint(player.magic_power - 5, player.magic_power + 5)
                    player.magic_power -= 10
                    monster.take_damage(damage)
                    ui_controller.draw_text(f"You cast a magic spell dealing {damage} damage!", 50, 300)
                else:
                    ui_controller.draw_text("Not enough magic power to cast a spell!", 50, 300)
            elif action == "3":
                # Use Item from Inventory
                if player.inventory.items:
                    ui_controller.draw_text("Select an item to use:", 50, 250)
                    for i, (item, quantity) in enumerate(player.inventory.items.items(), start=1):
                        ui_controller.draw_text(f"{i}. {item} - {quantity} available", 50, 300 + i * 50)

                    pygame.display.flip()

                    item_choice = None
                    while not (item_choice and 1 <= int(item_choice) <= len(player.inventory.items)):
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if pygame.K_1 <= event.key <= pygame.K_9:
                                    item_choice = pygame.key.name(event.key)

                    chosen_item = list(player.inventory.items.keys())[int(item_choice) - 1]
                    player.inventory.remove_item(chosen_item)
                    player.health += 20  # Example: Using a health potion to restore health
                    ui_controller.draw_text(f"You use a {chosen_item} to restore 20 health!", 50, 400)
                else:
                    ui_controller.draw_text("No items in the inventory!", 50, 300)

            # Monster's turn
            if monster.health > 0:
                monster_damage = random.randint(monster.attack - 3, monster.attack + 3)
                player.take_damage(monster_damage)
                ui_controller.draw_text(f"The {monster.name} attacks and deals {monster_damage} damage!", 50, 450)

            pygame.display.flip()
            pygame.time.delay(2000)

        # Combat results
        if player.health <= 0:
            ui_controller.draw_text("You were defeated!", 50, 500)
        else:
            ui_controller.draw_text(f"You defeated the {monster.name} and gained {monster.level * 10} experience!", 50, 500)
            player.gain_experience(monster.level * 10)
            player.inventory.add_item("Monster Tooth")  # Example: Adding a monster tooth to the inventory

        pygame.display.flip()
        pygame.time.delay(3000)