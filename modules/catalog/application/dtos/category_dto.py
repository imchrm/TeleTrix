from dataclasses import dataclass, field
from typing import Optional

""" This is a simple Data Transfer Object (DTO) pattern implemented as a Python dataclass. Here’s a breakdown:

Dataclass:
The class is decorated with @dataclass, which automatically generates special methods like __init__, __repr__, and __eq__.

Fields:

id: An optional integer field with a default value of None. It can represent the identifier of a category.
name: A string field with a default empty string. It represents the name of the category.
description: An optional string field with a default value of None. It can hold additional information about the category.
Overall, this DTO is used to encapsulate and transfer category data between application layers in a clean and structured way. """

"""
Data Transfer Object (DTO) for representing a category.

Attributes:
    id (Optional[int]): Unique identifier for the category. Defaults to None.
    name (str): The name of the category. Defaults to an empty string.
    description (Optional[str]): A brief description of the category. Defaults to None.

This class serves as a simple container for category-related data to streamline the exchange
of information across different parts of the application.
"""

@dataclass
class CategoryDTO:
    id: Optional[int] = field(default=None)
    name: str = field(default="")
    description: Optional[str] = field(default=None)