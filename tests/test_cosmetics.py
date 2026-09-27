from datetime import date, timedelta

from cosmetics import get_status, count_by_status, sort_cosmetics_by_name


def make_item(name="Крем", brand="Brand", months=6, opened=None, expiry=None):
    if expiry is None:
        expiry = date.today() + timedelta(days=365)
    return {
        "name": name,
        "brand": brand,
        "expiry": expiry.isoformat(),
        "months": months,
        "opened": opened,
    }


def test_status_not_opened():
    item = make_item()
    assert get_status(item) == "не вскрыто"


def test_status_expired_before_opening():
    item = make_item(expiry=date.today() - timedelta(days=1))
    assert "просрочено до вскрытия" in get_status(item)


def test_status_ok_after_opening():
    item = make_item(opened=date.today().isoformat(), months=6)
    assert "ок" in get_status(item)


def test_count_by_status():
    items = [make_item(), make_item()]
    stats = count_by_status(items)
    assert stats.get("не вскрыто") == 2


def test_sort_cosmetics_by_name():
    items = [make_item(name="Б"), make_item(name="А")]
    sorted_items = sort_cosmetics_by_name(items)
    assert sorted_items[0]["name"] == "А"
