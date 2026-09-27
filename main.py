from cosmetics import (
    add_cosmetic,
    open_cosmetic,
    show_list,
    show_reminders,
    find_cosmetics,
    sort_cosmetics_by_name,
    count_by_status,
)
from storage import load_cosmetics, save_cosmetics


def show_found(cosmetics: list[dict], query: str) -> None:
    found = find_cosmetics(cosmetics, query)
    if not found:
        print("Ничего не найдено.")
        return
    for item in found:
        print(f"• {item['brand']} {item['name']}")


def show_statistics(cosmetics: list[dict]) -> None:
    if not cosmetics:
        print("Список пуст.")
        return
    stats = count_by_status(cosmetics)
    print("\nСтатистика")
    for status, count in stats.items():
        print(f"{status}: {count}")


def main() -> None:
    cosmetics = load_cosmetics()

    menu = (
        "\nКонтроль сроков косметики\n"
        "1. Добавить средство\n"
        "2. Отметить вскрытие\n"
        "3. Показать список\n"
        "4. Напоминания\n"
        "5. Поиск\n"
        "6. Сортировка по названию\n"
        "7. Статистика\n"
        "0. Выход\n"
        "Выберите пункт: "
    )

    while True:
        choice = input(menu).strip()

        if choice == "1":
            add_cosmetic(cosmetics)
        elif choice == "2":
            open_cosmetic(cosmetics)
        elif choice == "3":
            show_list(cosmetics)
        elif choice == "4":
            show_reminders(cosmetics)
        elif choice == "5":
            query = input("Введите строку для поиска: ").strip()
            show_found(cosmetics, query)
        elif choice == "6":
            sorted_items = sort_cosmetics_by_name(cosmetics)
            for i, item in enumerate(sorted_items, start=1):
                print(f"{i}. {item['brand']} {item['name']}")
        elif choice == "7":
            show_statistics(cosmetics)
        elif choice == "0":
            save_cosmetics(cosmetics)
            print("До встречи!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
