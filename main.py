from functools import wraps
from typing import Dict, List, Tuple, Callable
from pathlib import Path
import pickle

from addressbook import AddressBook, Record
from notes import Note, NoteBook


DATA_DIR = Path.home() / ".personal_assistant"
DATA_FILE = DATA_DIR / "addressbook.pkl"

# Тіпізація для контактів, аргументів команд та розпарсеного вводу
Contacts = Dict[str, str]
CommandArgs = List[str]
ParsedInput = Tuple[str, CommandArgs]

# Зберігає адресну книгу у файл за допомогою pickle
def save_data(book: AddressBook, filename: Path = DATA_FILE) -> None:
    # Створюємо папку для даних, якщо її ще немає
    filename.parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "wb") as file:
        pickle.dump(book, file)

# Завантажує адресну книгу або створює нову, якщо файлу ще немає
def load_data(filename: Path = DATA_FILE) -> AddressBook:
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def input_error(func: Callable) -> Callable:
    # Декоратор для обробки помилок у функціях команд
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs) # Виклик оригінальної функції
        except IndexError: # Обробка помилки індексу (наприклад, недостатньо аргументів)
            return "Not enough arguments provided."
        except ValueError as error: # Обробка помилки значення (наприклад, неправильний формат даних)
            return str(error) if str(error) else "Invalid argument."
        except KeyError as error: # Обробка помилки ключа (наприклад, контакт не знайдено)
            return str(error).strip('"\'') if str(error) else "Contact not found."

    return inner

# Функції для обробки команд
def parse_input(user_input: str) -> ParsedInput:
    # Розділення вводу користувача на команду та аргументи
    parts = user_input.strip().split()

    # Перевірка на порожній ввід
    if not parts:
        return "", []

    # Витягування команди та аргументів
    command = parts[0].lower()
    args = parts[1:]

    # Повернення розпарсеного вводу
    return command, args

# Функції додачі контакту
@input_error
def add_contact(args: CommandArgs, book: AddressBook) -> str:
    # Перевірка на правильну кількість аргументів
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    # Витягування імені та телефону з аргументів
    name = args[0]
    phone = args[1]
    # Додавання нового контакту або оновлення наявного контакту
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added."
    else:
        record.add_phone(phone)
    # Повернення повідомлення про успішне додавання контакту
    return message

# Функції зміни контакту
@input_error
def change_contact(args: CommandArgs, book: AddressBook) -> str:
    # Перевірка на правильну кількість аргументів
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")

    # Витягування імені, старого та нового телефону з аргументів
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]

    # Перевірка наявності контакту та оновлення телефону
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    record.edit_phone(old_phone, new_phone)
    return f"Contact {name} updated."

# Функції показу телефону контакту
@input_error
def show_phone(args: CommandArgs, book: AddressBook) -> str:
    # Перевірка на правильну кількість аргументів
    if len(args) != 1:
        raise ValueError("Enter user name.")

    # Витягування імені з аргументів
    name = args[0]

    # Перевірка наявності контакту та повернення телефону
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    if not record.phones:
        return f"{name} has no phone numbers."
    phones = "; ".join(phone.value for phone in record.phones)
    return f"{name}: {phones}"

# Функції показу всіх контактів
@input_error
def show_all(book: AddressBook) -> str:
    # Перевірка наявності контактів
    if not book.data:
        raise KeyError # Додаю raise, щоб викликати обробку помилки у декораторі

    # Формування рядка з усіма контактами
    result = "Contacts:\n"
    for name, record in book.data.items():
        phones = "; ".join(phone.value for phone in record.phones)
        result += f"{name}: {phones}\n"
    return result.strip()

# Функція видалення контакту
@input_error
def delete_contact(args: CommandArgs, book: AddressBook) -> str:
    # Перевірка на правильну кількість аргументів
    if len(args) != 1:
        raise ValueError("Please provide the name of the contact.")

    name = args[0]

    # Видалення контакту або повідомлення про помилку
    if not book.delete(name):
        raise KeyError(f"Contact {name} not found.")

    return f"Contact {name} deleted."

# Функція додавання адреси контакту
@input_error
def add_address(args: CommandArgs, book: AddressBook) -> str:
    # Потрібно ввести ім'я та адресу
    if len(args) < 2:
        raise ValueError("Please provide the name and address.")

    name = args[0]
    address = " ".join(args[1:])

    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")

    record.add_address(address)
    return f"Address for {name} added."

# Функція додавання email контакту
@input_error
def add_email(args: CommandArgs, book: AddressBook) -> str:
    # Потрібно ввести ім'я та один email
    if len(args) != 2:
        raise ValueError("Please provide the name and email.")

    name, email = args

    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")

    record.add_email(email)
    return f"Email for {name} added."

@input_error
def add_birthday(args: CommandArgs, book: AddressBook) -> str:
    # Перевірка на правильну кількість аргументів
    if len(args) != 2:
        raise ValueError("Please provide both name and birthday in the format DD.MM.YYYY.")

    name, birthday = args
    # Перевірка наявності контакту та додавання дня народження
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    record.add_birthday(birthday)
    return f"Birthday for {name} added."

@input_error
def show_birthday(args: CommandArgs, book: AddressBook) -> str:
    # Перевірка на правильну кількість аргументів
    if len(args) != 1:
        raise ValueError("Please provide the name of the contact.")

    name = args[0]
    # Перевірка наявності контакту та повернення дня народження
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")

    if not hasattr(record, "birthday") or record.birthday is None:
        return "Birthday not set."

    return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args: CommandArgs, book: AddressBook) -> str:
    # Перевірка на правильну кількість аргументів
    if len(args) != 0:
        raise ValueError("This command does not take any arguments.")

    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in upcoming)

# Функція додавання нотатки
@input_error
def add_note(args: CommandArgs, notes: NoteBook) -> str:
    if not args:
        raise ValueError("Please provide note text.")

    text = " ".join(args)
    note = Note(text)
    notes.add_note(note)
    return f"Note added with id: {note.id}"

# Функція пошуку нотатки
@input_error
def find_note(args: CommandArgs, notes: NoteBook) -> str:
    if not args:
        raise ValueError("Please provide note id or text.")

    query = " ".join(args)
    found_notes = notes.find_note(query)
    if not found_notes:
        raise KeyError(f"Note {query} not found.")

    result = ""
    for note in found_notes:
        result += f"{note.id}: {note.text}\n"

    return result.strip()

# Функція редагування нотатки
@input_error
def edit_note(args: CommandArgs, notes: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Please provide note id and new text.")

    note_id = args[0]
    new_text = " ".join(args[1:])
    notes.edit_note(note_id, new_text)
    return "Note updated."

# Функція видалення нотатки
@input_error
def delete_note(args: CommandArgs, notes: NoteBook) -> str:
    if len(args) != 1:
        raise ValueError("Please provide note id.")

    notes.delete_note(args[0])
    return "Note deleted."

# Функція показу всіх нотаток
@input_error
def show_all_notes(args: CommandArgs, notes: NoteBook) -> str:
    if args:
        raise ValueError("This command does not take any arguments.")

    if not notes.data:
        return "No notes found."

    result = "Notes:\n"
    for note_id, note in notes.data.items():
        result += f"{note_id}: {note.text}\n"

    return result.strip()

def main():
    # Відновлення адресної книги з попереднього сеансу
    book = load_data()
    note_book = NoteBook()
    print("Welcome to the assistant bot!")

    # Запуск циклу для обробки команд користувача
    while True:
        # Отримання вводу користувача
        user_input = input("Enter a command: ")
        # Розпарсення вводу користувача
        command, args = parse_input(user_input)

        # Перевірка команди та виклик відповідної функції
        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "add-address":
            print(add_address(args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "add-note":
            print(add_note(args, note_book))

        elif command == "find-note":
            print(find_note(args, note_book))

        elif command == "edit-note":
            print(edit_note(args, note_book))

        elif command == "delete-note":
            print(delete_note(args, note_book))

        elif command == "all-notes":
            print(show_all_notes(args, note_book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
