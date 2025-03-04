from typing import Optional
from core.domain.entities.entity import Entity
from modules.catalog.domain.entities.category import Category

""" Below is an optimized version that addresses some potential issues and improves readability. In particular, it avoids using a mutable default argument by setting the default for category to None and then instantiating a new Category as needed. We also ensure type hints use Optional where a value may be missing. """

class Product(Entity):
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        photo: Optional[str] = None,
        quantity: int = 0,
        category: Optional[Category] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.photo = photo
        self.quantity = quantity
        self.category = category or Category()