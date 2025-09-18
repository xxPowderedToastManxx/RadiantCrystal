"""Adapter to expose a minimal UI used by controllers.

This module wraps the existing `UIController` (pygame-based) and
provides a small synchronous API used by `CombatController` and
unit-tests. In headless tests we can use the `DummyUI` instead.
"""

from typing import Sequence, Optional

import UIController
from EventHandler import EventHandler


class UIAdapter:
    def __init__(self, ui: UIController.UIController, event_handler: Optional[EventHandler] = None):
        self._ui = ui
        self._events = event_handler or EventHandler()

    def draw_text(self, text: str, x: int, y: int) -> None:
        # forward to UIController
        self._ui.draw_text(text, x, y)

    def wait_for_action(self, options: Sequence[str]) -> str:
        """Blocking chooser that uses EventHandler for input polling.

        Returns the chosen option string.
        """
        # draw options so the player can see them
        for i, opt in enumerate(options, start=1):
            self._ui.draw_text(f"{i}. {opt}", 50, 150 + i * 30)

        while True:
            events = self._events.poll()
            idx = self._events.numeric_choice(events, len(options))
            if idx is not None:
                return options[idx]

