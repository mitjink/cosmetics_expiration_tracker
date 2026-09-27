from datetime import date, timedelta

from models import Cosmetic, UsageRecord, User


def make_cosmetic() -> Cosmetic:
    return Cosmetic(
        cosmetic_id=1,
        name="Крем",
        brand="Brand",
        expiry=(date.today() + timedelta(days=365)).isoformat(),
        months=6,
    )


def make_user() -> User:
    return User(1, "Иван Петров", "ivan@example.com")


def test_record_creation():
    cosmetic = make_cosmetic()
    user = make_user()
    record = UsageRecord(
        record_id=1,
        cosmetic=cosmetic,
        user=user,
        opened_date=date.today().isoformat(),
    )
    assert record.id == 1
    assert record.cosmetic is cosmetic
    assert record.user is user
    assert not record.is_cancelled


def test_record_cancel():
    record = UsageRecord(
        record_id=1,
        cosmetic=make_cosmetic(),
        user=make_user(),
        opened_date=date.today().isoformat(),
    )
    record.cancel()
    assert record.is_cancelled


def test_record_to_dict_and_back():
    cosmetic = make_cosmetic()
    user = make_user()
    record = UsageRecord(
        record_id=1,
        cosmetic=cosmetic,
        user=user,
        opened_date=date.today().isoformat(),
    )
    data = record.to_dict()
    restored = UsageRecord.from_dict(data, [cosmetic], [user])
    assert restored is not None
    assert restored.id == record.id
    assert restored.cosmetic.id == cosmetic.id
    assert restored.user.id == user.id


def test_record_from_dict_missing_links():
    data = {
        "id": 1,
        "cosmetic_id": 99,
        "user_id": 99,
        "opened_date": date.today().isoformat(),
        "is_cancelled": False,
    }
    assert UsageRecord.from_dict(data, [], []) is None
