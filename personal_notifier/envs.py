import os

TELEGRAM_BOT_TOKEN_ENV_VARIABLE = 'PERSONAL_NOTIFIER_TELEGRAM_BOT_TOKEN'
PERSONAL_NOTIFIER_JSON_FILE_STORAGE_ENV_VARIABLE = 'PERSONAL_NOTIFIER_JSON_FILE_STORAGE'

_ALL_ENVS = [
    TELEGRAM_BOT_TOKEN_ENV_VARIABLE,
    PERSONAL_NOTIFIER_JSON_FILE_STORAGE_ENV_VARIABLE
]


def check_envs() -> bool:
    for env in _ALL_ENVS:
        if not os.environ.get(env, None):
            print(f"ENV variable is not set - {env}")
            return False

    return True


def get_env(name: str) -> str:
    return os.environ[name]
