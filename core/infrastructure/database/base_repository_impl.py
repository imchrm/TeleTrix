#Упрощенный пример класса для работы с inmemory бд, в реальности будет работа с конкретной БД.
#В данном случае используется словарь для хранения данных.
#В данном случае реализованы методы get_by_id, save, delete
class BaseRepositoryImpl:
    def __init__(self):
        self.db = {}

    #В методе get_by_id происходит получение данных по id из словаря
    def get_by_id(self, id):
        return self.db.get(id)

    #В методе save происходит сохранение данных в словарь
    def save(self, entity):
        self.db[entity.id] = entity
        return entity

    #В методе delete происходит удаление данных из словаря
    def delete(self, entity):
        if entity.id in self.db:
            del self.db[entity.id]