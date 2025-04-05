from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def save(self, product):
        pass

    @abstractmethod
    def delete(self, product):
        pass
