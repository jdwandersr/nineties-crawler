from src.player import get_default_party, Character
from src.combat import CombatEncounter


def test_combat_party_victory():
    party = get_default_party()
    enemies = [Character("Test Goblin", "Goblin", 1, 0)]
    combat = CombatEncounter(party, enemies)
    combat.party_action("attack", 0)
    assert enemies[0].hp <= 0