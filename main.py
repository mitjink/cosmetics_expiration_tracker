from datetime import date, datetime, timedelta

cosmetics = []

# Преобразует строку 'ГГГГ-ММ-ДД' в объект date.
def parse_date(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None

# Добавление нового косметического средства
def add_cosmetic():
    print("\nДобавление средства")
    name = input("Название: ").strip()
    brand = input("Бренд: ").strip()

    expiry_str = input("Срок годности до вскрытия (ГГГГ-ММ-ДД): ").strip()
    expiry = parse_date(expiry_str)
    if expiry < date.today():
        print("Внимание: срок годности до вскрытия уже истёк!")
    if expiry is None:
        print("Некорректная дата. Средство не добавлено.")
        return

    try:
        months = int(input("Срок использования после вскрытия (в месяцах): ").strip())
    except ValueError:
        print("Нужно ввести число. Средство не добавлено.")
        return

    item = {
        "name": name,
        "brand": brand,
        "expiry": expiry,
        "months": months,
        "opened": None,
    }
    cosmetics.append(item)
    print(f"Средство «{name}» добавлено.")

# Отметка даты вскрытия средства.
def open_cosmetic():
    print("\nОтметить вскрытие")
    if not cosmetics:
        print("Список пуст.")
        return

    show_list()
    try:
        index = int(input("Введите номер средства: ").strip()) - 1
        if index < 0 or index >= len(cosmetics):
            print("Неверный номер.")
            return
    except ValueError:
        print("Нужно ввести число.")
        return

    item = cosmetics[index]
    if item["expiry"] < date.today():
        print(f"Средство «{item['name']}» просрочено до вскрытия ({item['expiry']}). Вскрывать нельзя.")
        return
    if item["opened"] is not None:
        print(f"Средство уже вскрыто {item['opened']}.")
        return

    item["opened"] = date.today()
    deadline = item["opened"] + timedelta(days=item["months"] * 30)
    print(f"Средство «{item['name']}» вскрыто. Использовать до {deadline}.")

# Возвращает статус средства.
def get_status(item):
    if item["opened"] is None:
        if item["expiry"] < date.today():
            return "просрочено до вскрытия"
        return "не вскрыто"

    deadline = item["opened"] + timedelta(days=item["months"] * 30)
    days_left = (deadline - date.today()).days

    if days_left < 0:
        return f"ПРОСРОЧЕНО ({-days_left} дн. назад)"
    elif days_left <= 14:
        return f"скоро истекает ({days_left} дн.)"
    return f"ок ({days_left} дн.)"

# Показывает список всех средств.
def show_list():
    print("\nСписок средств")
    if not cosmetics:
        print("Список пуст.")
        return

    for i, item in enumerate(cosmetics, start=1):
        print(f"{i}. {item['brand']} {item['name']} {get_status(item)}")

# Показывает средства, срок которых истекает или уже истёк.
def show_reminders():
    print("\nНапоминания")
    found = False
    for item in cosmetics:
        status = get_status(item)
        if "ПРОСРОЧЕНО" in status or "скоро истекает" in status:
            print(f"• {item['brand']} {item['name']} — {status}")
            found = True
    if not found:
        print("Всё в порядке, напоминаний нет.")


def main():
    menu = (
        "\nКонтроль сроков косметики\n"
        "1. Добавить средство\n"
        "2. Отметить вскрытие\n"
        "3. Показать список\n"
        "4. Напоминания\n"
        "0. Выход\n"
        "Выберите пункт: "
    )

    while True:
        choice = input(menu).strip()

        if choice == "1":
            add_cosmetic()
        elif choice == "2":
            open_cosmetic()
        elif choice == "3":
            show_list()
        elif choice == "4":
            show_reminders()
        elif choice == "0":
            print("До встречи!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()