from .base_app_state import BaseAppState
from CombatController import CombatController
from EventHandler import EventHandler


class CombatState(BaseAppState):
    def __init__(self, ui_adapter, state_manager):
        super().__init__('combat', 'main_menu', state_manager)
        self.ui = ui_adapter
        self.event_handler = EventHandler()
        self.controller = CombatController()
        self.time_to_transition = False
        self._player_label = None
        self._monster_label = None

    def start(self):
        # For example purposes we'll create a dummy player and monster
        # In real usage these should be passed via incoming_transition_data
        player = self.incoming_transition_data.get('player')
        monster = self.incoming_transition_data.get('monster')
        if player is None or monster is None:
            # create simple stand-ins
            class P: pass
            class M: pass
            player = P()
            player.name = 'Hero'
            player.health = 20
            player.take_damage = lambda d: setattr(player, 'health', player.health - d)

            monster = M()
            monster.name = 'Goblin'
            monster.health = 6
            monster.take_damage = lambda d: setattr(monster, 'health', monster.health - d)

        self.controller.start(player, monster, self.ui)
        # create simple HUD labels if ui_manager available via adapter
        try:
            ui_manager = self.ui._ui_manager
            if ui_manager is not None:
                import pygame
                import pygame_gui
                from pygame_gui.elements.ui_label import UILabel
                # create labels; positions are arbitrary and can be tuned
                self._player_label = UILabel(pygame.Rect((20, 60), (200, 25)), f"Player HP: {getattr(player, 'health', '?')}", ui_manager)
                self._monster_label = UILabel(pygame.Rect((20, 90), (200, 25)), f"Monster HP: {getattr(monster, 'health', '?')}", ui_manager)
        except Exception:
            self._player_label = None
            self._monster_label = None

    def end(self):
        pass

    def run(self, surface, time_delta):
        # poll events and forward to controller
        events = self.event_handler.poll()
        for e in events:
            # forward UI button events to controller
            self.controller.handle_event(e)
            # process quitting
            import pygame
            if e.type == pygame.QUIT:
                self.time_to_quit_app = True

        # update controller
        self.controller.update(time_delta)

        # update HUD labels
        try:
            player = self.controller.player
            monster = self.controller.monster
            if self._player_label is not None:
                self._player_label.set_text(f"Player HP: {getattr(player, 'health', '?')}")
            if self._monster_label is not None:
                self._monster_label.set_text(f"Monster HP: {getattr(monster, 'health', '?')}")
        except Exception:
            # fallback: draw via adapter text
            try:
                if self.ui is not None:
                    p = self.controller.player
                    m = self.controller.monster
                    self.ui.draw_text(f"Player HP: {getattr(p, 'health', '?')}", 20, 60)
                    self.ui.draw_text(f"Monster HP: {getattr(m, 'health', '?')}", 20, 90)
            except Exception:
                pass

        # draw UI (controller draws via UI adapter)
        if self.controller.is_done():
            self.outgoing_transition_data = {'result': self.controller.get_result()}
            self.set_target_state_name('main_menu')
            self.trigger_transition()

