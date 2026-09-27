from datetime import date
from typing import Optional
from models import Cosmetic, User, UsageRecord
from storage import (
    load_cosmetics,
    load_records,
    load_users,
    save_cosmetics,
    save_records,
    save_users,
)
from utils import input_date, input_int, input_non_empty


def next_id(items: list) -> int:
    if not items:
        return 1
    return max(item.id for item in items) + 1


def find_cosmetic_by_id(
    cosmetics: list[Cosmetic],
    cosmetic_id: int,
) -> Optional[Cosmetic]:
    return next((c for c in cosmetics if c.id == cosmetic_id), None)


def find_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    return next((u for u in users if u.id == user_id), None)


def add_cosmetic(cosmetics: list[Cosmetic]) -> None:
    print("\nДобавление средства")
    name = input_non_empty("Название: ")
    brand = input_non_empty("Бренд: ")
    expiry = input_date("Срок годности до вскрытия (ГГГГ-ММ-ДД): ")
    months = input_int("Срок использования после вскрытия (в месяцах): ")

    if expiry < date.today():
        print("Внимание: срок годности до вскрытия уже истёк.")

    cosmetic = Cosmetic(
        cosmetic_id=next_id(cosmetics),
        name=name,
        brand=brand,
        expiry=expiry.isoformat(),
        months=months,
    )
    cosmetics.append(cosmetic)
    print(f"Средство «{name}» добавлено.")


def add_user(users: list[User]) -> None:
    print("\nДобавление пользователя")
    name = input_non_empty("Имя: ")
    email = input_non_empty("Email: ")
    user = User(user_id=next_id(users), name=name, email=email)
    users.append(user)
    print(f"Пользователь «{name}» добавлен.")


def open_cosmetic(
    cosmetics: list[Cosmetic],
    users: list[User],
    records: list[UsageRecord],
) -> None:
    print("\nОтметить вскрытие")
    if not cosmetics or not users:
        print("Нужны хотя бы одно средство и один пользователь.")
        return

    show_cosmetics(cosmetics)
    cosmetic_id = input_int("Введите номер средства: ")
    cosmetic = find_cosmetic_by_id(cosmetics, cosmetic_id)
    if cosmetic is None:
        print("Средство не найдено.")
        return

    if cosmetic.is_expired_before_opening():
        print(f"Средство «{cosmetic.name}» просрочено до вскрытия. "
              "Вскрывать нельзя.")
        return

    if cosmetic.is_opened():
        print(f"Средство уже вскрыто {cosmetic.opened}.")
        return

    show_users(users)
    user_id = input_int("Введите номер пользователя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден.")
        return

    cosmetic.open()
    record = UsageRecord(
        record_id=next_id(records),
        cosmetic=cosmetic,
        user=user,
        opened_date=cosmetic.opened,
    )
    records.append(record)
    deadline = cosmetic.get_deadline()
    print(f"Средство «{cosmetic.name}» вскрыто. Использовать до {deadline}.")


def cancel_record(records: list[UsageRecord]) -> None:
    print("\nОтмена записи")
    if not records:
        print("Записей нет.")
        return
    show_records(records)
    record_id = input_int("Введите номер записи: ")
    record = next((r for r in records if r.id == record_id), None)
    if record is None:
        print("Запись не найдена.")
        return
    if record.is_cancelled:
        print("Запись уже отменена.")
        return
    record.cancel()
    print(f"Запись №{record.id} отменена.")


def show_cosmetics(cosmetics: list[Cosmetic]) -> None:
    print("\nСписок средств")
    if not cosmetics:
        print("Список пуст.")
        return
    for cosmetic in cosmetics:
        print(f"{cosmetic.id}. {cosmetic}")


def show_users(users: list[User]) -> None:
    print("\nСписок пользователей")
    if not users:
        print("Список пуст.")
        return
    for user in users:
        print(f"{user.id}. {user}")


def show_records(records: list[UsageRecord]) -> None:
    print("\nЗаписи об использовании")
    if not records:
        print("Записей нет.")
        return
    for record in records:
        print(record)


def show_reminders(cosmetics: list[Cosmetic]) -> None:
    print("\nНапоминания")
    found = False
    for cosmetic in cosmetics:
        status = cosmetic.get_status()
        if Cosmetic.STATUS_EXPIRED in status or Cosmetic.STATUS_SOON in status:
            print(f"• {cosmetic.brand} {cosmetic.name} — {status}")
            found = True
    if not found:
        print("Всё в порядке, напоминаний нет.")


def main() -> None:
    cosmetics = load_cosmetics()
    users = load_users()
    records = load_records(cosmetics, users)

    menu = (
        "\nКонтроль сроков косметики\n"
        "1. Добавить средство\n"
        "2. Добавить пользователя\n"
        "3. Отметить вскрытие\n"
        "4. Показать средства\n"
        "5. Показать пользователей\n"
        "6. Показать записи\n"
        "7. Напоминания\n"
        "8. Отменить запись\n"
        "0. Выход\n"
        "Выберите пункт: "
    )

    while True:
        choice = input(menu).strip()

        if choice == "1":
            add_cosmetic(cosmetics)
        elif choice == "2":
            add_user(users)
        elif choice == "3":
            open_cosmetic(cosmetics, users, records)
        elif choice == "4":
            show_cosmetics(cosmetics)
        elif choice == "5":
            show_users(users)
        elif choice == "6":
            show_records(records)
        elif choice == "7":
            show_reminders(cosmetics)
        elif choice == "8":
            cancel_record(records)
        elif choice == "0":
            save_cosmetics(cosmetics)
            save_users(users)
            save_records(records)
            print("До встречи!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
