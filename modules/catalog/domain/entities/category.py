from core.domain.entities.entity import Entity


class Category(Entity):
    def __init__(self, value: str=None, description: str=None):
        self.value = value
        self.description = description