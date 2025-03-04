import yaml
import os

def load_config(config_path="core/config/config.yaml"):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_config():
    if not hasattr(get_config, '_config'):
        get_config._config = load_config()
    return get_config._config

def get_telegram_bot_token():
    config = get_config()
    token_env_var_name = config['telegram_bot']['token_env_var']
    return os.environ.get(token_env_var_name)

if __name__ == '__main__':
    config = get_config()
    print(config)
    telegram_token = get_telegram_bot_token()
    print(f"Telegram Token (from env): {telegram_token}")