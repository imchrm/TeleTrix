from typing import Optional
from aiogram import types as aiogram_types
from core.application.menu.menu_dto import MenuDTO


class MenuStates:
    # TODO: Add more states
    UNAUTHORIZED = "UNAUTHORIZED"
    AUTHORIZED = "AUTHORIZED"

    pass

class Commands():
    START = 'start'
    AUTH = 'auth'
    HELP = 'help'
    REGISTER = 'register'
    PROFILE = 'profile'
    CATALOG = 'catalog'
    PRODUCT = 'product'
    PRODUCTS = 'products'
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
                aiogram_types.BotCommand(command=Commands.START, description='Старт'),
                aiogram_types.BotCommand(command=Commands.PRODUCTS, description='Каталог'),
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

