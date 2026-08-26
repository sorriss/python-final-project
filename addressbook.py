import re
from collections import UserDict
from datetime import datetime, timedelta

# Клас для представлення поля (Field)
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для представлення імені контакту
class Name(Field):
    def __init__(self, value):
        # Перевірка на порожнє значення імені
        if not value or not str(value).strip():
            raise ValueError("Ім'я контакту є обов'язковим.")
        # Використовуємо метод батьківського класу для ініціалізації значення
        super().__init__(str(value).strip())

# Клас для представлення номера телефону
class Phone(Field):
    def __init__(self, value):
        value = str(value).strip()
        # Перевірка значення телефону
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Номер телефону повинен містити рівно 10 цифр.")
        # Використовуємо метод батьківського класу для ініціалізації значення
        super().__init__(value)

# Клас для представлення email
class Email(Field):
    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, value):
        value = str(value).strip()
        if not self.EMAIL_PATTERN.match(value):
            raise ValueError("Email повинен бути у форматі example@domain.com.")
        super().__init__(value)

# Клас для представлення дня народження
class Birthday(Field):
    def __init__(self, value):
        try:
            date_value = datetime.strptime(str(value).strip(), "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Дата народження повинна бути у форматі ДД.ММ.РРРР.")
        super().__init__(date_value)

# Клас для представлення адреси
class Address(Field):
    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Адреса не може бути порожньою.")
        super().__init__(str(value).strip())

# Клас для представлення запису контакту
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.emails = []

    # Додаємо телефон до запису
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Видаляємо телефон з запису
    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            return True
        return False

    # Редагуємо телефон у записі
    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = self.find_phone(old_phone)
        # Перевірка наявності старого телефону перед редагуванням
        if not old_phone_obj:
            raise ValueError(f"Телефон {old_phone} не знайдено.")
        # Валідація нового телефону через Phone
        new_phone_obj = Phone(new_phone)
        old_phone_obj.value = new_phone_obj.value

    # Знаходимо телефон у записі
    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    # Додаємо email до запису
    def add_email(self, email):
        self.emails.append(Email(email))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # Додаємо/оновлюємо адресу запису
    def add_address(self, address):
        self.address = Address(address)

    # Повертаємо рядкове представлення запису
    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        address_str = f", address: {self.address.value}" if self.address else ""
        emails_str = f", emails: {'; '.join(e.value for e in self.emails)}" if self.emails else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}{address_str}{emails_str}"

# Клас для представлення адресної книги
class AddressBook(UserDict):
    # Додаємо запис до адресної книги
    def add_record(self, record):
        self.data[record.name.value] = record

    # Знаходимо запис за іменем
    def find(self, name):
        return self.data.get(name)

    # Видаляємо запис за іменем
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value
            try:
                birthday_this_year = birthday.replace(year=today.year)
            except ValueError:
                birthday_this_year = birthday.replace(year=today.year, day=28)

            # Якщо день народження вже пройшов цього року, використовую наступний рік
            if birthday_this_year < today:
                try:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                except ValueError:
                    birthday_this_year = birthday.replace(year=today.year + 1, day=28)

            # Розраховую різницю в днях між сьогоднішньою датою та днем народження
            days_diff = (birthday_this_year - today).days

            # Перевіряю, чи день народження користувача відбудеться протягом наступних 7 днів
            if 0 <= days_diff <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:  # Якщо день народження в суботу
                    congratulation_date += timedelta(days=2)  # Переносимо на понеділок
                elif congratulation_date.weekday() == 6:  # Якщо день народження в неділю
                    congratulation_date += timedelta(days=1)  # Переносимо на понеділок

                upcoming.append({
                    'name': record.name.value,
                    'congratulation_date': congratulation_date.strftime('%Y.%m.%d')
                })

        return upcoming

if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("15.08.1990")
    john_record.add_address("вул. Хрещатик 1, Київ")
    assert "address: вул. Хрещатик 1, Київ" in str(john_record)
    john_record.add_email("john@example.com")
    assert "emails: john@example.com" in str(john_record)
    try:
        john_record.add_email("not-an-email")
        raise AssertionError("Некоректний email мав бути відхилений.")
    except ValueError:
        pass

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("18.08.1992")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    print("Upcoming birthdays:", book.get_upcoming_birthdays())

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
