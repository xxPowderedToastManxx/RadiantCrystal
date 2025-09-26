import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel

from .base_app_state import BaseAppState


from Player import Player
from monster_factory import _ensure_cache, random_monster
from ui_adapter import UIAdapter
from Monster import Monster
from .combat_state import CombatState


class LoadState(BaseAppState):
    def __init__(self, ui_manager: pygame_gui.UIManager, state_manger):
        super().__init__('load_state', 'main_menu', state_manger)

        self.ui_manager = ui_manager
        self._buttons = []

    def start(self):
        # create buttons for each monster in the monsters.json
        monsters = _ensure_cache()
        x = 50
        y = 150
        for m in monsters:
            btn = pygame_gui.elements.ui_button.UIButton(pygame.Rect((x, y), (200, 30)), m.get('name', 'Monster'), self.ui_manager)
            self._buttons.append((btn, m))
            y += 35

        # cancel/back button
        self.back_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect((50, y + 20), (100, 30)), 'Back', self.ui_manager)
        self._buttons.append((self.back_button, None))

    def end(self):
        for b, _ in self._buttons:
            try:
                b.kill()
            except Exception:
                pass
        self._buttons = []

    def run(self, surface, time_delta):
        import pygame
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for b, m in self._buttons:
                    if event.ui_element == b:
                        if m is None:
                            self.set_target_state_name('main_menu')
                            self.trigger_transition()
                            return
                        # start combat with chosen monster
                        ui_adapter = UIAdapter(None, None, self.ui_manager)
                        player = Player('Hero')
                        monster = Monster(m.get('name'), m.get('level', 1), m.get('stats'), m.get('hp'), m.get('attack_bonus', 0))
                        combat_state = CombatState(ui_adapter, self.state_manager)
                        combat_state.incoming_transition_data = {'player': player, 'monster': monster}
                        self.set_target_state_name('combat')
                        self.trigger_transition()
                        return

        self.ui_manager.process_events(event)
        self.ui_manager.update(time_delta)
        surface.fill((0, 0, 0))
        self.ui_manager.draw_ui(surface)


