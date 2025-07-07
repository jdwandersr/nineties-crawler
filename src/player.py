from typing import List


class Character:
    def __init__(
        self, name: str, char_class: str, hp: int, sp: int, lvl: int = 1
    ) -> None:
        self.name = name
        self.char_class = char_class
        self.hp = hp
        self.max_hp = hp
        self.sp = sp
        self.max_sp = sp
        self.lvl = lvl
        self.xp = 0

    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)

    def restore_sp(self, amount: int) -> None:
        self.sp = min(self.max_sp, self.sp + amount)

    def is_alive(self) -> bool:
        return self.hp > 0


def get_default_party() -> List[Character]:
    return [
        Character("Rogar", "Fighter", 20, 0),
        Character("Shade", "Thief", 16, 0),
        Character("Lyria", "Cleric", 14, 10),
        Character("Mira", "Wizard", 10, 14),
    ]