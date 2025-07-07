from src.entities import get_default_mobs


def test_default_mobs_exist():
    mobs = get_default_mobs()
    assert len(mobs) >= 3
    names = [m.name for m in mobs]
    assert "Goblin" in names
    assert "Boss Ogre" in names