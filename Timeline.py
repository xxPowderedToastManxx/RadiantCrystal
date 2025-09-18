
import RadiantCrystal

import Player as player

import Actions as actions

import pygame
import UIController as ui_controller


class Timeline:

    # Function to handle story events
    def story_event(event):
        global player_health, player_experience, miles_traveled # this probably shouldn't be global, check for in mulitple scripts

        ui_controller.draw_text(event["description"], 50, 300)
        pygame.display.flip()
        pygame.time.delay(1000)

        for choice in event["choices"]:
            ui_controller.draw_text(f"{choice['choice_id']}. {choice['text']}", 50, 350 + choice['choice_id'] * 50)

        pygame.display.flip()

        player_choice = None
        while player_choice not in [str(choice['choice_id']) for choice in event["choices"]]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    player_choice = pygame.key.name(event.key)

        chosen_choice = next(choice for choice in event["choices"] if choice["choice_id"] == int(player_choice))

        # Apply consequences of the chosen choice
        if "experience_gain" in chosen_choice:
            player_experience += chosen_choice["experience_gain"]
        if "information_gain" in chosen_choice:
            ui_controller.draw_text(f"You learn: {chosen_choice['information_gain']}", 50, 450)
            pygame.display.flip()
            pygame.time.delay(2000)
        if "health_loss" in chosen_choice:
            player_health -= chosen_choice["health_loss"]
        if "miles_saved" in chosen_choice:
            miles_traveled -= chosen_choice["miles_saved"]
        if "combat" in chosen_choice and chosen_choice["combat"]:
            # Trigger combat
            actions.combat("Monster", 1, 30, 15)


