from typing import List
from modules.user.domain.entities.user import User
from modules.user.domain.repositories.user_repository import UserRepository
from modules.user.infrastructure.database.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, user_model: UserModel):
        self.user_model = user_model

    def create(self, user: User) -> User:
        return self.user_model.create(user)

    def get(self, user_id: int) -> User:
        return self.user_model.get(user_id)

    def get_all(self) -> List[User]:
        return self.user_model.get_all()

    def update(self, user: User) -> User:
        return self.user_model.update(user)

    def delete(self, user_id: int) -> None:
        return self.user_model.delete(user_id)
    