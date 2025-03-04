from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def delete(self, entity):
        pass
