"""Small D&D-like mechanics helpers used by the game.

Functions:
- ability_mod(score): returns the standard D&D ability modifier for a score.
- proficiency_bonus(level): simple proficiency by level table.
- roll_d20(controller, advantage=0): roll a d20 with advantage/disadvantage.
- resolve_attack(attacker, defender, dice_controller, attack_bonus=0): performs an attack roll
  and returns (hit: bool, roll: int, total: int, damage: int).
"""
from typing import Tuple, Optional


def ability_mod(score: int) -> int:
    """Return ability modifier for a given ability score.

    Formula: floor((score - 10) / 2)
    """
    return (score - 10) // 2


def proficiency_bonus(level: int) -> int:
    """Return a simple proficiency bonus based on level.

    Uses the common 5e table: 1-4: +2, 5-8: +3, 9-12: +4, 13-16: +5, 17+: +6
    """
    if level < 5:
        return 2
    if level < 9:
        return 3
    if level < 13:
        return 4
    if level < 17:
        return 5
    return 6


def roll_d20(dice_controller, advantage: int = 0) -> Tuple[int, int]:
    """Roll a d20 using provided dice_controller.

    advantage: 0 = normal, 1 = advantage, -1 = disadvantage
    Returns (best_roll, other_roll) where other_roll==best_roll for normal.
    """
    r1 = dice_controller.roll_d20()
    if advantage == 0:
        return r1, r1
    r2 = dice_controller.roll_d20()
    if advantage > 0:
        return (r1, r2) if r1 >= r2 else (r2, r1)
    else:
        # disadvantage -> return lowest as first
        return (r1, r2) if r1 <= r2 else (r2, r1)


def resolve_attack(attacker, defender, dice_controller, attack_bonus: int = 0, advantage: int = 0) -> Tuple[bool, int, int, int]:
    """Resolve a simple attack.

    - attacker: object with `.attack` or attack bonus; if not present attack_bonus param is used
    - defender: object with `.ac` attribute
    - dice_controller: provides roll_d20() and a damage die method `roll_d6` (fallback)

    Returns (hit, roll, total, damage)
    """
    atk_bonus = getattr(attacker, "attack", 0) + attack_bonus
    best, other = roll_d20(dice_controller, advantage)
    roll = best
    total = roll + atk_bonus

    def get_damage_from_attacker(atk, dc, critical: bool = False) -> int:
        # Player with equipped weapon
        if hasattr(atk, 'equipped_weapon') and getattr(atk, 'equipped_weapon') is not None:
            # build temporary Monster to reuse damage logic
            from Monster import Monster
            tmp = Monster('tmp', damage_die_spec=getattr(atk.equipped_weapon, 'damage_die', None))
            if critical:
                return tmp.damage_die_with_controller(dc) + tmp.damage_die_with_controller(dc)
            return tmp.damage_die_with_controller(dc)

        # attacker provides damage_die_with_controller
        if hasattr(atk, 'damage_die_with_controller') and callable(atk.damage_die_with_controller):
            if critical:
                return atk.damage_die_with_controller(dc) + atk.damage_die_with_controller(dc)
            return atk.damage_die_with_controller(dc)

        # legacy damage_die callable
        if hasattr(atk, 'damage_die') and callable(atk.damage_die):
            if critical:
                return atk.damage_die() + atk.damage_die()
            return atk.damage_die()

        # fallback default d6
        if critical:
            return dc.roll_d6() + dc.roll_d6()
        return dc.roll_d6()

    # Natural 20 is a critical hit: always hits and doubles damage dice
    if roll == 20:
        hit = True
        dmg = get_damage_from_attacker(attacker, dice_controller, critical=True)
        return hit, roll, total, dmg

    # Natural 1 is an automatic miss
    if roll == 1:
        return False, roll, total, 0

    hit = total >= getattr(defender, "ac", 10)
    if not hit:
        return False, roll, total, 0

    dmg = get_damage_from_attacker(attacker, dice_controller, critical=False)
    return True, roll, total, dmg
