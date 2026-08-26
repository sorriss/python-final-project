import uuid
from collections import UserDict


class Note:
    def __init__(self, text):
        # Зберігаємо текст нотатки
        self.text = text

        # Для кожної нотатки створюємо унікальний id
        self.id = str(uuid.uuid4())

        # Список тегів нотатки
        self.tags = []

    # Додаємо тег до нотатки, уникаючи дублікатів
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)


class NoteBook(UserDict):
    # Додаємо нотатку до словника
    def add_note(self, note):
        self.data[note.id] = note

    # Шукаємо нотатку за id або точним текстом
    def find_note(self, query):
        if query in self.data:
            return self.data[query]

        for note in self.data.values():
            if note.text == query:
                return note

        return None

    # Видаляємо нотатку за id
    def delete_note(self, note_id):
        if note_id not in self.data:
            raise KeyError(f"Note {note_id} not found.")

        del self.data[note_id]

    # Змінюємо текст нотатки за id
    def edit_note(self, note_id, new_text):
        if note_id not in self.data:
            raise KeyError(f"Note {note_id} not found.")

        self.data[note_id].text = new_text
