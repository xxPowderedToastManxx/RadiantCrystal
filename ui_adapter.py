"""Adapter to expose a minimal UI used by controllers.

This module wraps the existing `UIController` (pygame-based) and
provides a small synchronous API used by `CombatController` and
unit-tests. In headless tests we can use the `DummyUI` instead.
"""

from typing import Sequence, Optional

import UIController
from EventHandler import EventHandler
import pygame

try:
    import pygame_gui
    from pygame_gui.elements.ui_button import UIButton
except Exception:
    pygame_gui = None


class UIAdapter:
    def __init__(self, ui: UIController.UIController, event_handler: Optional[EventHandler] = None, ui_manager=None):
        self._ui = ui
        self._events = event_handler or EventHandler()
        self._ui_manager = ui_manager

    def draw_text(self, text: str, x: int, y: int) -> None:
        # forward to UIController
        self._ui.draw_text(text, x, y)

    def wait_for_action(self, options: Sequence[str]) -> str:
        """Blocking chooser that uses EventHandler for input polling.

        If a `ui_manager` (pygame_gui.UIManager) was provided, present
        temporary buttons and wait for their press events. Otherwise fall
        back to numeric key polling via `EventHandler`.
        """
        # draw options so the player can see them
        for i, opt in enumerate(options, start=1):
            self._ui.draw_text(f"{i}. {opt}", 50, 150 + i * 30)

        # If a UI manager is available, create buttons and wait for their press
        buttons = []
        if self._ui_manager is not None and pygame_gui is not None:
            for i, opt in enumerate(options, start=1):
                btn = UIButton(pygame.Rect((50, 150 + i * 30), (200, 30)), opt, self._ui_manager)
                buttons.append(btn)

            # event loop until a button press
            while True:
                events = self._events.poll()
                for e in events:
                    if e.type == pygame_gui.UI_BUTTON_PRESSED:
                        for b, opt in zip(buttons, options):
                            if e.ui_element == b:
                                # cleanup
                                for bb in buttons:
                                    bb.kill()
                                return opt

        # fallback: numeric keys
        while True:
            events = self._events.poll()
            idx = self._events.numeric_choice(events, len(options))
            if idx is not None:
                return options[idx]

