class UserDTO:
    def __init__(self, name: str, phone: str, telegram_id:int):
        self.name = name
        self.phone = phone
        self.telegram_id = telegram_id
        pass

    def set_name(self, name):
        self.name = name
        return self

