from typing import List, Tuple, Optional, Dict
import random


class Tile:
    def __init__(self, walkable: bool = True, has_clue: bool = False) -> None:
        self.walkable = walkable
        self.has_clue = has_clue


class Dungeon:
    def __init__(self, width: int = 20, height: int = 15) -> None:
        self.width = width
        self.height = height
        self.grid: List[List[Tile]] = [
            [Tile(random.choice([True, True, False])) for _ in range(width)]
            for _ in range(height)
        ]
        self.clues: Dict[Tuple[int, int], str] = {}
        self._generate_clues()

    def _generate_clues(self) -> None:
        # Place 3-5 clues at random walkable tiles
        num_clues = random.randint(3, 5)
        placed = 0
        while placed < num_clues:
            x, y = random.randrange(self.width), random.randrange(self.height)
            if self.grid[y][x].walkable and (x, y) not in self.clues:
                self.grid[y][x].has_clue = True
                self.clues[(x, y)] = f"Clue {placed+1}: Something cryptic."
                placed += 1

    def get_clue(self, x: int, y: int) -> Optional[str]:
        return self.clues.get((x, y))