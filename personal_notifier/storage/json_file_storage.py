import json
from typing import List

from personal_notifier.envs import get_env, PERSONAL_NOTIFIER_JSON_FILE_STORAGE_ENV_VARIABLE
from personal_notifier.model.user import User


class JsonFileStorage:
    def __init__(self, file_name: str) -> None:
        self._file_name = file_name

    def load_users(self) -> List[User]:
        with open(self._file_name, 'r', encoding='utf-8') as file:
            json_list = json.load(file)
            return list(
                map(
                    lambda user_json: User.from_json(user_json),
                    json_list
                )
            )

    def save_users(self, users: List[User]) -> None:
        with open(self._file_name, 'w', encoding='utf-8') as file:
            json_list = list(
                map(
                    lambda user: user.to_json(),
                    users
                )
            )
            json.dump(json_list, file, ensure_ascii=False)

    @staticmethod
    def default():
        return JsonFileStorage(file_name=get_env(PERSONAL_NOTIFIER_JSON_FILE_STORAGE_ENV_VARIABLE))
