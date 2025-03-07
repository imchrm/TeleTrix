from typing import Optional
from aiogram import types as aiogram_types
from core.application.menu.menu_dto import MenuDTO


class MenuStates:
    UNAUTHORIZED = 'unauthorized'
    AUTHORIZED = 'authorized'

class Commands():
    AUTH = 'auth'
    HELP = 'help'
    REGISTER = 'register'
    PROFILE = 'profile'
    CATALOG = 'catalog'
    PRODUCT = 'product'
    LOGOUT = 'logout'

class MenuConfig():
    def start(self) -> MenuDTO:
      return self.get_menu_by_state(MenuStates.UNAUTHORIZED)

    def get_menu_by_state(self, state: Optional[str]=MenuStates.UNAUTHORIZED) -> MenuDTO:
        self.state = state
        #  Логика определения меню в зависимости от состояния
        if state == MenuStates.UNAUTHORIZED:
            return MenuDTO(
                commands=[
                aiogram_types.BotCommand(command=Commands.AUTH, description='Авторизация'),
                aiogram_types.BotCommand(command=Commands.HELP, description='Помощь'),
                ]
            )
        elif state == MenuStates.AUTHORIZED:
            return MenuDTO(
                commands=[
                    aiogram_types.BotCommand(command=Commands.CATALOG, description='Каталог'),
                    aiogram_types.BotCommand(command=Commands.PRODUCT, description='Тест'),
                    aiogram_types.BotCommand(command=Commands.PROFILE, description='Профиль'),
                    aiogram_types.BotCommand(command=Commands.LOGOUT, description='Выход'),
                ]
            )

