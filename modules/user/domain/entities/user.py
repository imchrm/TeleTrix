from core.domain.entities.entity import Entity


class User(Entity):
    def __init__(self, name: str, phone: str, telegram_id: str):
        self.name = name
        self.phone = phone
        self.telegram_id = telegram_id
        self.id = None