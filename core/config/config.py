import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar, Optional

class StorageSettings(BaseSettings):
    storage_type: Optional[str] = None
    
class DatabaseSettings(BaseSettings):
    engine: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    name: str = "crm_db"
    user: str = "db_user"
    password: Optional[str] = None  # Пароль может быть задан через переменную окружения

class AdminTelegramBotSettings(BaseSettings):
    token_env_var: ClassVar[str] = "ADMIN_TELEGRAM_BOT_TOKEN"
    token: Optional[str] = None # Токен будет загружен из переменной окружения

class TelegramBotSettings(BaseSettings):
    token_env_var: ClassVar[str] = "TELEGRAM_BOT_TOKEN"
    token: Optional[str] = None # Токен будет загружен из переменной окружения

class LoggingSettings(BaseSettings):
    level: str = "DEBUG"
    format: str = '%(asctime)s - %(levelname)s - %(message)s'


class AppSettings(BaseSettings):
    name: str = "TELETRIX CRM System"
    debug: bool = True

class Config(BaseSettings):
    storage: StorageSettings = StorageSettings()
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    telegram_bot: TelegramBotSettings = TelegramBotSettings()
    admin_telegram_bot: AdminTelegramBotSettings = AdminTelegramBotSettings()
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(
        config_path='config.yaml', # Путь к файлу конфигурации
        env_file='.env', # Путь к .env файлу
        env_nested_delimiter='_', # Разделитель для вложенных переменных окружения
        extra='ignore' # Игнорировать лишние поля в файле и переменных
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.storage.storage_type is None:
            self.storage.storage_type = os.environ.get('STORAGE_TYPE')
        self.telegram_bot.token = os.environ.get(self.telegram_bot.token_env_var)
        self.admin_telegram_bot.token = os.environ.get(self.admin_telegram_bot.token_env_var)   
        self.database.password = os.environ.get('DB_PASSWORD')


class ConfigManager:
    _instance: Optional["ConfigManager"] = None
    _config: Config

    def __init__(self) -> None:
        self._config = Config()

    @classmethod
    def instance(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def config(self) -> Config:
        return self._config

    def reset_config(self) -> None:
        self._config = Config()

def get_config() -> Config:
    return ConfigManager.instance().config

if __name__ == '__main__':
    config = get_config()
    print(config)
    print(f"Database URL: {config.database.engine}://{config.database.user}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.name}")
    print(f"Telegram Token: {config.telegram_bot.token}")
    print(f"Admin Telegram Token: {config.admin_telegram_bot.token}")