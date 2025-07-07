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
        # Simple attack: party deals damage to target enemy
        if self.party and self.enemies and target_idx < len(self.enemies):
            alive_party = [p for p in self.party if p.is_alive()]
            if alive_party:
                damage = 3 + (len(alive_party) - 1)  # More damage with more alive party members
                self.enemies[target_idx].hp -= damage

    def enemy_action(self) -> None:
        # All alive enemies attack first alive party member
        for enemy in self.enemies:
            if enemy.is_alive():
                for p in self.party:
                    if p.is_alive():
                        # Use enemy's attack value if available, otherwise default to 2
                        damage = getattr(enemy, 'atk', 2)
                        p.hp -= damage
                        break