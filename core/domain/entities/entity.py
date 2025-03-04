from abc import ABC

# Assuming Entity is either defined here or imported from another module.
# For this example, we'll define a simple Entity base class.

class Entity(ABC):
        def __init__(self, id=None):
            self.id = id

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.id == other.id
            return False

        def __hash__(self):
            return hash(self.id)

