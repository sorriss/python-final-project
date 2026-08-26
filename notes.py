import uuid
from collections import UserDict


class Note:
    def __init__(self, text):
        # Зберігаємо текст нотатки
        self.text = text

        # Для кожної нотатки створюємо унікальний id
        self.id = str(uuid.uuid4())


class NoteBook(UserDict):
    # Додаємо нотатку до словника
    def add_note(self, note):
        self.data[note.id] = note

    # Шукаємо нотатки за id або частиною тексту
    def find_note(self, query):
        if query in self.data:
            return [self.data[query]]

        found_notes = []
        query_lower = query.lower()
        for note in self.data.values():
            if query_lower in note.text.lower():
                found_notes.append(note)

        return found_notes

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
