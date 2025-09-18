"""Minimal combat controller.

This class implements a simple turn-based combat loop but avoids
direct pygame drawing calls. Instead it expects a UI-like object with
`draw_text` and `wait_for_action` methods and a dice controller for
rolls. This makes the controller testable and avoids global helper
functions.
"""

from __future__ import annotations

from typing import List

import random

from DiceController import DiceController


class CombatController:
    def __init__(self, ui_controller, dice: DiceController | None = None) -> None:
        """Create a combat controller.

        ui_controller must provide at least:
          - draw_text(text, x, y)
          - wait_for_action(options) -> selected option string
        """
        self.ui = ui_controller
        self.dice = dice or DiceController()

    def combat(self, player, monster) -> dict:
        """Run a simple combat between a single player and a single monster.

        Returns a result dict: {'winner': 'player'|'monster', 'player': player, 'monster': monster}
        """
        self.ui.draw_text(f"A wild {monster.name} appears!", 50, 300)

        while player.health > 0 and monster.health > 0:
            self.ui.draw_text("Choose your action:", 50, 100)
            options = ["Attack", "Cast Spell", "Use Item"]
            choice = self.ui.wait_for_action(options)

            if choice == "Attack":
                attack_roll = self.dice.roll_d20()
                if attack_roll >= 10:
                    damage = self.dice.roll_d6()
                    monster.take_damage(damage)
                    self.ui.draw_text(f"You hit the {monster.name} for {damage} damage!", 50, 300)
                else:
                    self.ui.draw_text(f"You miss the {monster.name}!", 50, 300)
            elif choice == "Cast Spell":
                spell_roll = self.dice.roll_d20()
                if spell_roll >= 12:
                    damage = self.dice.roll_d8()
                    monster.take_damage(damage)
                    self.ui.draw_text(f"You cast a spell and deal {damage} damage!", 50, 300)
                else:
                    self.ui.draw_text("Your spell fails to hit the target.", 50, 300)
            elif choice == "Use Item":
                # Defer item usage to UI/inventory for now
                self.ui.draw_text("You rummage your bag but find nothing useful.", 50, 300)
            else:
                self.ui.draw_text("Invalid action.", 50, 300)

            # Monster's turn
            if monster.health > 0:
                monster_attack_roll = self.dice.roll_d20()
                if monster_attack_roll >= 10:
                    monster_damage = self.dice.roll_d6()
                    player.take_damage(monster_damage)
                    self.ui.draw_text(f"The {monster.name} hits you for {monster_damage} damage!", 50, 450)
                else:
                    self.ui.draw_text(f"The {monster.name} misses you!", 50, 450)

        winner = "player" if player.health > 0 else "monster"
        return {"winner": winner, "player": player, "monster": monster}
