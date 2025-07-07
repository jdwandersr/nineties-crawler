from typing import List
from src.player import Character


class CombatEncounter:
    def __init__(self, party: List[Character], enemies: List[Character]) -> None:
        self.party = party
        self.enemies = enemies
        self.turn = 0  # 0 for party, 1 for enemies

    def is_over(self) -> bool:
        return all(not e.is_alive() for e in self.enemies) or all(
            not p.is_alive() for p in self.party
        )

    def next_turn(self) -> None:
        self.turn = 1 - self.turn

    def party_action(self, action: str, target_idx: int = 0) -> None:
        # Placeholder: just attack first enemy
        if self.party and self.enemies:
            self.enemies[target_idx].hp -= 3

    def enemy_action(self) -> None:
        # Placeholder: all enemies attack first alive party member
        for enemy in self.enemies:
            if enemy.is_alive():
                for p in self.party:
                    if p.is_alive():
                        p.hp -= 2
                        break