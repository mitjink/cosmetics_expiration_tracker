from datetime import date, timedelta

from models import Cosmetic


def make_cosmetic(**kwargs) -> Cosmetic:
    defaults = {
        "cosmetic_id": 1,
        "name": "Крем",
        "brand": "Brand",
        "expiry": (date.today() + timedelta(days=365)).isoformat(),
        "months": 6,
        "opened": None,
    }
    defaults.update(kwargs)
    return Cosmetic(**defaults)


def test_cosmetic_creation():
    cosmetic = make_cosmetic()
    assert cosmetic.id == 1
    assert cosmetic.name == "Крем"
    assert cosmetic.brand == "Brand"
    assert cosmetic.opened is None


def test_cosmetic_is_not_opened():
    cosmetic = make_cosmetic()
    assert not cosmetic.is_opened()


def test_cosmetic_expired_before_opening():
    cosmetic = make_cosmetic(
        expiry=(date.today() - timedelta(days=1)).isoformat()
    )
    assert cosmetic.is_expired_before_opening()
    assert cosmetic.get_status() == Cosmetic.STATUS_EXPIRED_BEFORE


def test_cosmetic_open():
    cosmetic = make_cosmetic()
    cosmetic.open()
    assert cosmetic.is_opened()
    assert cosmetic.get_deadline() is not None


def test_cosmetic_status_ok():
    cosmetic = make_cosmetic()
    cosmetic.open()
    assert Cosmetic.STATUS_OK in cosmetic.get_status()


def test_cosmetic_to_dict_and_back():
    cosmetic = make_cosmetic()
    data = cosmetic.to_dict()
    restored = Cosmetic.from_dict(data)
    assert restored.id == cosmetic.id
    assert restored.name == cosmetic.name
    assert restored.brand == cosmetic.brand


def test_cosmetic_str():
    cosmetic = make_cosmetic()
    text = str(cosmetic)
    assert "Крем" in text
    assert "не вскрыто" in text
