"""Simple centralized event handler wrapper around pygame events.

This module provides a tiny helper class to poll pygame events and
interpret simple choices (numeric key selection, quit). It keeps logic
out of app states and UI adapters.
"""

import pygame
from typing import List, Optional


class EventHandler:
    def __init__(self) -> None:
        pass

    def poll(self) -> List[pygame.event.EventType]:
        """Return the list of pygame events since last call."""
        return list(pygame.event.get())

    def is_quit(self, events: List[pygame.event.EventType]) -> bool:
        for e in events:
            if e.type == pygame.QUIT:
                return True
        return False

    def numeric_choice(self, events: List[pygame.event.EventType], max_choice: int) -> Optional[int]:
        """If a numeric key corresponding to 1..max_choice was pressed,
        return zero-based index, otherwise None."""
        for e in events:
            if e.type == pygame.KEYDOWN:
                key = e.key
                if 49 <= key <= 57:  # '1'..'9'
                    idx = key - 49
                    if 0 <= idx < max_choice:
                        return idx
        return None
