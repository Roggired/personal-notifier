import asyncio

from personal_notifier.telegram_bot import notify_about_time_management
from personal_notifier.dialogue import morning_notification, evening_notification
from personal_notifier.storage.json_file_storage import JsonFileStorage


def notify_all_users(
    is_morning: bool
) -> None:
    json_file_storage = JsonFileStorage.default()
    all_users = json_file_storage.load_users()

    if len(all_users) <= 0:
        return

    for user in all_users:
        notification: str
        if is_morning:
            notification = morning_notification(user)
        else:
            notification = evening_notification(user)

        asyncio.run(notify_about_time_management(user, notification))
