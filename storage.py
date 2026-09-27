import json
import os

from models import Cosmetic, User, UsageRecord

DATA_DIR = "data"
COSMETICS_FILE = os.path.join(DATA_DIR, "cosmetics.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
RECORDS_FILE = os.path.join(DATA_DIR, "records.json")


def _load_json(filename: str) -> list[dict]:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Ошибка загрузки {filename}: {exc}")
        return []


def _save_json(filename: str, data: list[dict]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"Ошибка сохранения {filename}: {exc}")


def load_cosmetics(filename: str = COSMETICS_FILE) -> list[Cosmetic]:
    return [Cosmetic.from_dict(item) for item in _load_json(filename)]


def save_cosmetics(
    cosmetics: list[Cosmetic],
    filename: str = COSMETICS_FILE,
) -> None:
    _save_json(filename, [c.to_dict() for c in cosmetics])


def load_users(filename: str = USERS_FILE) -> list[User]:
    return [User.from_dict(item) for item in _load_json(filename)]


def save_users(users: list[User], filename: str = USERS_FILE) -> None:
    _save_json(filename, [u.to_dict() for u in users])


def load_records(
    cosmetics: list[Cosmetic],
    users: list[User],
    filename: str = RECORDS_FILE,
) -> list[UsageRecord]:
    records = []
    for item in _load_json(filename):
        record = UsageRecord.from_dict(item, cosmetics, users)
        if record is not None:
            records.append(record)
    return records


def save_records(
    records: list[UsageRecord],
    filename: str = RECORDS_FILE,
) -> None:
    _save_json(filename, [r.to_dict() for r in records])
