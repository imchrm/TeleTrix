from typing import Any, Dict
from core.infrastructure.file.structure import StructureBase


class ProductStructure(StructureBase):
    prefix_of_path = "storage/"
    @classmethod
    def load_products(cls) -> Dict[str, Any]:
        return cls.load_yaml(cls.get_config_path(ProductStructure.prefix_of_path + File + "products.yaml"))

class CategoryStructure(StructureBase):
    @classmethod
    def load_categories(cls) -> Dict[str, Any]:
        return cls.load_yaml(cls.get_config_path(ProductStructure.prefix_of_path + "categories.yaml"))

class UserStructure(StructureBase):
    @classmethod
    def load_users(cls) -> Dict[str, Any]:
        return cls.load_yaml(cls.get_config_path(ProductStructure.prefix_of_path + "users.yaml"))