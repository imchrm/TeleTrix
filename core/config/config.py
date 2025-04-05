"""Module providing a configaration functionality of application."""

from __future__ import annotations
from ast import IsNot
import logging as log
import os
from typing import Any, ClassVar, Literal, Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ConfigUtils:
    """Utility class for configuration management."""
    @staticmethod
    def parse_env_var(env_var_name: str) -> str:
        """Parse and return the value of an environment variable."""
        value = os.getenv(env_var_name)
        if value is None:
            raise ValueError(f"Environment variable {env_var_name} not found")
        return value
    
    @staticmethod
    def get_nested_value(data: dict, path: str) -> str:
        """Get a nested value from a dictionary using a dot-separated path."""
        parts = path.split(".")
        for part in parts:
            data = data.get(part, {})
        if not isinstance(data, str):
            raise ValueError(f"Parse error!\nExpected a string value by path: {path}, probably got an object: {type(data)}")
        return data

class FileStorageSettings(BaseModel):
    """Settings for file storage."""
    path: str = Field(..., description="Path to the storage directory")
    data_file_type: Literal["yaml", "json"] = Field(..., description="Type of data file: yaml or json")
    categories: str = Field(..., description="File name for categories data")
    products: str = Field(..., description="File name for products data")
    users: str = Field(..., description="File name for users data")
    orders: str = Field(..., description="File name for orders data")
    order_items: str = Field(..., description="File name for order items data")

class DatabaseStorageSettings(BaseModel):
    """Settings for database storage."""
    engine: str = Field(..., description="Database engine")
    url: str = Field(..., description="Database host")
    port: int = Field(..., description="Database port")
    name: str = Field(..., description="Database name")
    user: str = Field(..., description="Database user")
    password: str = Field(..., description="Database password")


class StorageSettings(BaseModel):
    """Settings for storage."""
    file: Optional[FileStorageSettings] = Field(None, description="Settings for file storage")
    database: Optional[DatabaseStorageSettings] = Field(None, description="Settings for database storage")

class TBSettings(BaseSettings):
    """ Settings for Telegram bot. """
    path: ClassVar[str | None] = None # Path for telegram bot token environment variable
    token: Optional[str] = Field(default='', description="Telegram bot token (loaded later)")  # Токен будет загружен из переменной окружения

    # model_config = SettingsConfigDict(env_prefix="TELEGRAM_BOT_")

class CustomerTBSettings(TBSettings):
    """ Settings for the customer Telegram bot. """
    path: ClassVar[str | None] =  "telegram.bot.customer.token_env_var"

class AdminTBSettings(TBSettings):
    """ Settings for the admin Telegram bot. """
    path:ClassVar[str | None] =  "telegram.bot.admin.token_env_var"


class AppSettings(BaseModel):
    """ Application settings. """
    name: str = "TeleTrix CRM System"
    debug: bool = True


class Config(BaseSettings):
    """ Application configuration settings. """

    is_model_validate: bool = False
    data: ClassVar[dict] = {}
    app: ClassVar[AppSettings] = AppSettings()
    customer_telegram_bot: TBSettings = CustomerTBSettings()  # Provide default values
    admin_telegram_bot: AdminTBSettings = AdminTBSettings()
    storage: StorageSettings = StorageSettings(
        file=FileStorageSettings(
            path='',
            data_file_type='yaml',
            categories='',
            products='',
            users='',
            orders='',
            order_items=''
        ),
        database=DatabaseStorageSettings(
            engine='',
            url='',
            port=0,
            name='',
            user='',
            password=''
        )
    )

    model_config = SettingsConfigDict(
        # commented out the env_file to avoid confusion when loading the config twice (see on load_dotenv() below)
        # env_file=".env",  # Changed from ".inv" to ".env" which is more standard
        env_file_encoding="utf-8",  # Added encoding
        env_nested_delimiter="_",  # Changed to double underscore for better separation
        env_prefix="",  # Added prefix for environment variables
        case_sensitive=False,  # Added for case-insensitive env vars
        extra="allow",  # Allow extra fields
    )

    def __init__(self, **data):
        log.info("-----------call __init__()-----------")
        super().__init__(**data)

    def model_post_init(self, __context: Any) -> None:
        log.info("-----------call model_post_init()-----------")

        data = ConfigManager.instance().data

        def set_token(settings: TBSettings, env_var_name_path:Optional[str | None]=None) -> None:
            if env_var_name_path is None:
                raise ValueError("Parse data to Config ERROR: env_var_name_path cannot be None")
            env_var_name = ConfigUtils.get_nested_value(data, env_var_name_path)
            settings.token = ConfigUtils.parse_env_var(env_var_name)
            log.info(f"Settings env_var_name: {env_var_name}, token: {settings.token}")
            
        try:
            set_token(self.customer_telegram_bot, "telegram.bot.customer.token_env_var")
            set_token(self.admin_telegram_bot, "telegram.bot.admin.token_env_var")
        except (FileNotFoundError, yaml.YAMLError) as e:
            log.error(f"Error loading or parsing config.yaml: {e}")

class ConfigManager:
    """Singleton class for managing application configuration."""

    __slots__ = ('_config', '_data', '_config_loaded')
    _instance: Optional["ConfigManager"] = None
    # _config_loaded: Optional[bool] = False

    def __init__(self) -> None:
        """Initialize ConfigManager with empty config and data."""
        if ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.instance() instead")
        self._config = None
        self._data: dict = {}
        self._config_loaded: bool = False
        # Implicitly load configuration
        # default_config_path = "config.yaml"
        # self.load_config(default_config_path)

    @classmethod
    def instance(cls) -> "ConfigManager":
        """Get singleton instance of ConfigManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def config(self) -> Config:
        """Get current configuration."""

        if not self._config_loaded:
            default_config_path = "config.yaml"
            self.load_config(default_config_path)
            self._config_loaded = True

        if self._config is None:
            raise RuntimeError("Config not initialized")
        return self._config

    @property
    def data(self) -> dict:
        """Get raw configuration data."""
        return self._data

    @data.setter
    def data(self, value: dict) -> None:
        """Set raw configuration data."""
        self._data = value

    def set_config(self, config: Config) -> None:
        """Set current configuration."""
        self._config = config

    def reset(self) -> None:
        """Reset configuration to default state."""
        self._config = None
        self._data = {}
        
    def load_config(self, file_path: str) -> None:
        """Load configuration from YAML file."""
        log.debug("Loading configuration from %s", file_path)
        load_dotenv()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            self.data = config_data
            config = Config.model_validate(config_data)
            ConfigManager.instance().set_config(config)
        except FileNotFoundError:
            log.error(f"Configuration file not found: {file_path}")
            raise
        except yaml.YAMLError as e:
            log.error(f"Error parsing YAML file: {e}")
            raise
        except ValidationError as e:
            log.error("Validation error: %s", e)
            raise
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            raise
        
    def __del__(self) -> None:
        """Destructor for ConfigManager."""
        log.info("ConfigManager instance is being deleted.")
        self.reset()
        
    def __repr__(self) -> str:
        """String representation of ConfigManager."""
        return f"ConfigManager(config={self._config}, data={self._data})"
    
    def __str__(self) -> str:
        """String representation of ConfigManager."""
        return f"ConfigManager(config={self._config}, data={self._data})"
    
    def __enter__(self) -> ConfigManager:
        """Enter context manager."""
        return self

def get_config() -> Config :
    return ConfigManager.instance().config

def load_config(file_path: str) -> Config:
    """Load configuration from YAML file."""
    load_dotenv()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        ConfigManager.instance().data = config_data
        config = Config.model_validate(config_data)
        ConfigManager.instance().set_config(config)

        return config
    except FileNotFoundError:
        log.error(f"Configuration file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        log.error(f"Error parsing YAML file: {e}")
        raise
    except ValidationError as e:
        log.error("Validation error: %s", e)
        raise


if __name__ == "__main__":
    try:
        # config = load_config("config.yaml")
        # ConfigManager.instance().load_config("config.yaml")
        config = ConfigManager.instance().config
        
        log.info(f"App Name: {config.app.name}" )
        log.info(f"Debug Mode: {config.app.debug}" )
        log.info(f"Telegram Bot Token: {config.customer_telegram_bot.token}" )
        log.info(f"Admin Telegram Bot Token: {config.admin_telegram_bot.token}" )
        if config.storage.file:
            log.info(f"File Storage Path: {config.storage.file.path}" )
            log.info(f"Data File Type: {config.storage.file.data_file_type}" )
            log.info(f"Categories File:{config.storage.file.categories}" )
            log.info(f"Products File: {config.storage.file.products}" )
            log.info(f"Users File: {config.storage.file.users}" )
            log.info(f"Orders File: {config.storage.file.orders}" )
            log.info(f"Order Items File: {config.storage.file.order_items}" )
        else:
            log.info("No file storage settings found.")
        if config.storage.database:
            log.info(f"Database Engine: {config.storage.database.engine}" )
            log.info(f"Database URL: {config.storage.database.url}" )
            log.info(f"Database Port: {config.storage.database.port}" )
            log.info(f"Database Name: {config.storage.database.name}" )
            log.info(f"Database User: {config.storage.database.user}" )
            log.info(f"Database Password: {config.storage.database.password}" )
        else:
            log.info("No database storage settings found.")
    except Exception as e:
        log.info("An error occurred: %s", e)
        raise
