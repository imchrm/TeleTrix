from typing import List
from aiogram import types as aiogram_types

class MenuDTO:
  def __init__(self, commands:List[aiogram_types.BotCommand]):
    self.commands = commands

  def get_commands(self)-> List[aiogram_types.BotCommand]:
    return self.commands