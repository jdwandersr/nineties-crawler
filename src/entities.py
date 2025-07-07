from typing import List


class Mob:
    def __init__(self, name: str, hp: int, atk: int) -> None:
        self.name = name
        self.hp = hp
        self.atk = atk

    def is_alive(self) -> bool:
        return self.hp > 0


def get_default_mobs() -> List[Mob]:
    return [
        Mob("Goblin", 6, 2),
        Mob("Skeleton", 8, 3),
        Mob("Orc", 12, 4),
        Mob("Boss Ogre", 24, 6),
    ]