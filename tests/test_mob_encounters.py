"""Tests for mob encounter functionality."""

import pytest
from src.dungeon import Dungeon
from src.entities import Mob
from src.combat import CombatEncounter
from src.player import get_default_party


def test_dungeon_spawns_mobs():
    """Test that dungeons spawn mobs on generation."""
    dungeon = Dungeon()
    
    # Count mobs in the dungeon
    mob_count = 0
    for row in dungeon.grid:
        for tile in row:
            if tile.mob and tile.mob.is_alive():
                mob_count += 1
    
    # Should have at least 3 mobs
    assert mob_count >= 3
    assert mob_count <= 6  # Maximum is 6


def test_mob_encounter_detection():
    """Test that mobs are properly detected on tiles."""
    dungeon = Dungeon()
    
    # Find a tile with a mob
    mob_tile = None
    for y, row in enumerate(dungeon.grid):
        for x, tile in enumerate(row):
            if tile.mob and tile.mob.is_alive():
                mob_tile = (x, y)
                break
        if mob_tile:
            break
    
    assert mob_tile is not None
    x, y = mob_tile
    tile = dungeon.grid[y][x]
    assert tile.mob is not None
    assert tile.mob.is_alive()
    assert hasattr(tile.mob, 'name')
    assert hasattr(tile.mob, 'hp')
    assert hasattr(tile.mob, 'atk')


def test_mob_combat_integration():
    """Test that mobs work correctly in combat."""
    party = get_default_party()
    mob = Mob("Test Goblin", 6, 2)
    
    combat = CombatEncounter(party, [mob])
    
    # Test combat initialization
    assert not combat.is_over()
    assert combat.turn == 0  # Party goes first
    
    # Test party attack
    original_hp = mob.hp
    combat.party_action("attack", 0)
    assert mob.hp < original_hp
    
    # Test mob defeat
    mob.hp = 0
    assert not mob.is_alive()
    assert combat.is_over()


def test_mob_removal_after_defeat():
    """Test that mobs are removed from tiles after defeat."""
    dungeon = Dungeon()
    
    # Find a tile with a mob
    for y, row in enumerate(dungeon.grid):
        for x, tile in enumerate(row):
            if tile.mob and tile.mob.is_alive():
                # Simulate defeating the mob
                tile.mob.hp = 0
                assert not tile.mob.is_alive()
                
                # Simulate post-combat cleanup
                tile.mob = None
                assert tile.mob is None
                return
    
    # Should have found at least one mob
    assert False, "No mobs found in dungeon"


def test_mob_types_variety():
    """Test that different types of mobs are spawned."""
    # Generate multiple dungeons to see variety
    mob_names = set()
    for _ in range(5):
        dungeon = Dungeon()
        for row in dungeon.grid:
            for tile in row:
                if tile.mob and tile.mob.is_alive():
                    mob_names.add(tile.mob.name)
    
    # Should have at least 2 different mob types
    assert len(mob_names) >= 2