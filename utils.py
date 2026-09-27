from datetime import date, datetime


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Нужно ввести число. Попробуйте снова.")


def input_date(prompt: str) -> date:
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("Неверный формат даты. Пример: 2006-09-21")


def input_not_empty(prompt: str) -> str:
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Поле не может быть пустым.")
