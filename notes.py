import uuid


class Note:
    def __init__(self, text):
        # Зберігаємо текст нотатки
        self.text = text

        # Для кожної нотатки створюємо унікальний id
        self.id = str(uuid.uuid4())
