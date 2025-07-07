from typing import List


class Mob:
    """
    Represents a hostile creature that can be encountered in the dungeon.
    
    Mobs have basic combat stats and can engage in battle with the player's party.
    They are compatible with the combat system and can be placed on dungeon tiles.
    
    Attributes:
        name (str): The mob's display name
        hp (int): Current health points
        max_hp (int): Maximum health points
        atk (int): Attack damage value
    """
    def __init__(self, name: str, hp: int, atk: int) -> None:
        self.name = name
        self.hp = hp
        self.max_hp = hp  # Add max_hp for consistency with Character
        self.atk = atk

    def is_alive(self) -> bool:
        """Check if the mob is still alive (has HP > 0)."""
        return self.hp > 0


def get_default_mobs() -> List[Mob]:
    return [
        Mob("Goblin", 6, 2),
        Mob("Skeleton", 8, 3),
        Mob("Orc", 12, 4),
        Mob("Boss Ogre", 24, 6),
    ]