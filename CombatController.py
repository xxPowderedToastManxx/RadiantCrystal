"""Event-driven combat controller.

This controller exposes a small state machine so app states can start
combat, forward events to it, and call update each frame. It creates
buttons through the UI adapter and reacts to button-press events.
"""

from __future__ import annotations

from typing import Optional
import random

from DiceController import DiceController
from mechanics import resolve_attack


class CombatController:
    def __init__(self, dice: Optional[DiceController] = None) -> None:
        self.dice = dice or DiceController()
        self.ui = None
        self.player = None
        self.monster = None
        self._buttons = []
        self._state = "idle"  # idle, awaiting_player, monster_turn, finished
        self._result = None

    def start(self, player, monster, ui_adapter) -> None:
        self.player = player
        self.monster = monster
        self.ui = ui_adapter
        self._state = "awaiting_player"
        self.ui.draw_text(f"A wild {monster.name} appears!", 50, 300)
        self._show_player_options()

    def _show_player_options(self) -> None:
        options = ["Attack", "Cast Spell", "Use Item"]
        # create buttons using the adapter (if available)
        try:
            self._buttons = self.ui.create_buttons(options)
        except Exception:
            self._buttons = []

    def handle_event(self, event) -> None:
        """Handle a pygame or pygame_gui event forwarded from the app state."""
        # handle button presses from pygame_gui
        import pygame_gui

        if hasattr(pygame_gui, "UI_BUTTON_PRESSED") and event.type == pygame_gui.UI_BUTTON_PRESSED:
            # find which button
            for b, opt in zip(self._buttons, ["Attack", "Cast Spell", "Use Item"]):
                if event.ui_element == b:
                    self._on_player_choice(opt)
                    return

    def _on_player_choice(self, choice: str) -> None:
        if choice == "Attack":
            hit, roll, total, damage = resolve_attack(self.player, self.monster, self.dice)
            if hit:
                self.monster.take_damage(damage)
                self.ui.draw_text(f"You hit the {self.monster.name} for {damage} damage! (roll {roll} total {total})", 50, 300)
            else:
                self.ui.draw_text(f"You miss the {self.monster.name}! (roll {roll} total {total})", 50, 300)
        elif choice == "Cast Spell":
            spell_roll = self.dice.roll_d20()
            if spell_roll >= 12:
                damage = self.dice.roll_d8()
                self.monster.take_damage(damage)
                self.ui.draw_text(f"You cast a spell and deal {damage} damage!", 50, 300)
            else:
                self.ui.draw_text("Your spell fails to hit the target.", 50, 300)
        elif choice == "Use Item":
            self.ui.draw_text("You rummage your bag but find nothing useful.", 50, 300)

        # remove buttons after choice
        try:
            self.ui.remove_buttons(self._buttons)
        except Exception:
            pass
        self._buttons = []

        # check if monster died
        if self.monster.health <= 0:
            self._finish("player")
            return

        # go to monster turn
        self._state = "monster_turn"

    def update(self, dt: float) -> None:
        """Called each frame by the app state. Handles monster turn when appropriate."""
        if self._state == "monster_turn":
            # resolve monster attack using mechanics
            hit, roll, total, damage = resolve_attack(self.monster, self.player, self.dice)
            if hit:
                self.player.take_damage(damage)
                self.ui.draw_text(f"The {self.monster.name} hits you for {damage} damage! (roll {roll} total {total})", 50, 450)
            else:
                self.ui.draw_text(f"The {self.monster.name} misses you! (roll {roll} total {total})", 50, 450)

            if self.player.health <= 0:
                self._finish("monster")
                return

            # otherwise return to player
            self._state = "awaiting_player"
            self._show_player_options()

    def is_done(self) -> bool:
        return self._state == "finished"

    def _finish(self, winner: str) -> None:
        self._state = "finished"
        self._result = {"winner": winner, "player": self.player, "monster": self.monster}

    def get_result(self):
        return self._result

