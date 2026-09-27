import json
import os

DATA_DIR = "data"
COSMETICS_FILE = os.path.join(DATA_DIR, "cosmetics.json")


def load_cosmetics(filename: str = COSMETICS_FILE) -> list[dict]:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Ошибка загрузки данных: {exc}")
        return []


def save_cosmetics(cosmetics: list[dict], filename: str = COSMETICS_FILE) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(cosmetics, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"Ошибка сохранения данных: {exc}")
