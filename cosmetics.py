from datetime import date, timedelta

from utils import input_int, input_date, input_not_empty

STATUS_OK = "ок"
STATUS_SOON = "скоро истекает"
STATUS_EXPIRED = "ПРОСРОЧЕНО"
STATUS_NOT_OPENED = "не вскрыто"
STATUS_EXPIRED_BEFORE = "просрочено до вскрытия"


def add_cosmetic(cosmetics: list[dict]) -> None:
    print("\nДобавление средства")
    name = input_not_empty("Название: ")
    brand = input_not_empty("Бренд: ")
    expiry = input_date("Срок годности до вскрытия (ГГГГ-ММ-ДД): ")
    months = input_int("Срок использования после вскрытия (в месяцах): ")

    if expiry < date.today():
        print("Внимание: срок годности до вскрытия уже истёк.")

    item = {
        "name": name,
        "brand": brand,
        "expiry": expiry.isoformat(),
        "months": months,
        "opened": None,
    }
    cosmetics.append(item)
    print(f"Средство «{name}» добавлено.")


def get_status(item: dict) -> str:
    expiry = date.fromisoformat(item["expiry"])
    opened_raw = item.get("opened")

    if opened_raw is None:
        if expiry < date.today():
            return STATUS_EXPIRED_BEFORE
        return STATUS_NOT_OPENED

    opened = date.fromisoformat(opened_raw)
    deadline = opened + timedelta(days=item["months"] * 30)
    days_left = (deadline - date.today()).days

    if days_left < 0:
        return f"{STATUS_EXPIRED} ({-days_left} дн. назад)"
    if days_left <= 14:
        return f"{STATUS_SOON} ({days_left} дн.)"
    return f"{STATUS_OK} ({days_left} дн.)"


def open_cosmetic(cosmetics: list[dict]) -> None:
    print("\nОтметить вскрытие")
    if not cosmetics:
        print("Список пуст.")
        return

    show_list(cosmetics)
    index = input_int("Введите номер средства: ") - 1
    if index < 0 or index >= len(cosmetics):
        print("Неверный номер.")
        return

    item = cosmetics[index]
    expiry = date.fromisoformat(item["expiry"])

    if expiry < date.today():
        print(f"Средство «{item['name']}» просрочено до вскрытия ({expiry}). Вскрывать нельзя.")
        return

    if item["opened"] is not None:
        print(f"Средство уже вскрыто {item['opened']}.")
        return

    item["opened"] = date.today().isoformat()
    deadline = date.today() + timedelta(days=item["months"] * 30)
    print(f"Средство «{item['name']}» вскрыто. Использовать до {deadline}.")


def show_list(cosmetics: list[dict]) -> None:
    print("\nСписок средств")
    if not cosmetics:
        print("Список пуст.")
        return
    for i, item in enumerate(cosmetics, start=1):
        print(f"{i}. {item['brand']} {item['name']} — {get_status(item)}")


def show_reminders(cosmetics: list[dict]) -> None:
    print("\nНапоминания")
    found = False
    for item in cosmetics:
        status = get_status(item)
        if STATUS_EXPIRED in status or STATUS_SOON in status:
            print(f"• {item['brand']} {item['name']} — {status}")
            found = True
    if not found:
        print("Всё в порядке, напоминаний нет.")


def find_cosmetics(cosmetics: list[dict], query: str) -> list[dict]:
    query_lower = query.lower()
    return [
        item for item in cosmetics
        if query_lower in item["name"].lower()
        or query_lower in item["brand"].lower()
    ]


def sort_cosmetics_by_name(cosmetics: list[dict]) -> list[dict]:
    return sorted(cosmetics, key=lambda item: item["name"].lower())


def count_by_status(cosmetics: list[dict]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in cosmetics:
        status = get_status(item)
        if STATUS_EXPIRED in status:
            key = "просрочено"
        elif STATUS_SOON in status:
            key = "скоро истекает"
        elif STATUS_EXPIRED_BEFORE in status:
            key = "просрочено до вскрытия"
        elif STATUS_NOT_OPENED in status:
            key = "не вскрыто"
        else:
            key = "ок"
        result[key] = result.get(key, 0) + 1
    return result
