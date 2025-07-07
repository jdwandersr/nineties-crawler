from src.dungeon import Dungeon


def test_dungeon_clues_not_empty():
    dungeon = Dungeon()
    assert len(dungeon.clues) > 0
    for (x, y), text in dungeon.clues.items():
        assert isinstance(text, str)
        assert dungeon.grid[y][x].has_clue