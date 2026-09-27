import os
import tempfile

from storage import load_cosmetics, save_cosmetics


def test_save_and_load():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "data.json")
        items = [{"name": "Крем", "brand": "Brand", "expiry": "2026-12-31", "months": 6, "opened": None}]
        save_cosmetics(items, path)
        loaded = load_cosmetics(path)
        assert loaded == items


def test_load_missing_file():
    assert load_cosmetics("no_such_file.json") == []
