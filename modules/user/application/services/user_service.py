from modules.user.application.dtos.user_dto import UserDTO

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, user_dto: UserDTO):
        """Регистрация нового пользователя."""
        user = User(
            name=user_dto.name,
            phone=user_dto.phone,
            telegram_id=user_dto.telegram_id
        )
        self.user_repository.save(user)
        return user

    def get_user_by_id(self, user_id: int):
        """Получение пользователя по ID."""
        return self.user_repository.get_by_id(user_id)

    # Другие методы для работы с пользователями...