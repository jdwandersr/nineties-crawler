from src.player import get_default_party


def test_default_party_size():
    party = get_default_party()
    assert len(party) == 4
    names = [c.name for c in party]
    assert "Rogar" in names
    assert "Mira" in names