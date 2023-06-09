import sys

from personal_notifier.envs import check_envs
from personal_notifier.notify import notify_all_users
from personal_notifier.telegram_bot import start_personal_notifier_long_polling_bot

USAGE_STR = "python main.py --mode notify m(or e) or python main.py --bot"


if __name__ == '__main__':
    if not check_envs():
        exit(1)

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"Invalid params. Usage: {USAGE_STR}")
        exit(1)

    if sys.argv[1] != '--mode':
        print(f"Invalid params. Usage: {USAGE_STR}")
        exit(1)

    if sys.argv[2] != 'notify' and sys.argv[2] != 'bot':
        print(f"Invalid params. Usage: {USAGE_STR}")
        exit(1)

    mode = sys.argv[2]

    if mode == 'bot':
        if len(sys.argv) != 3:
            print(f"Invalid params. Usage: {USAGE_STR}")
            exit(1)
        start_personal_notifier_long_polling_bot()

    if mode == 'notify':
        if len(sys.argv) != 4:
            print(f"Invalid params. Usage: {USAGE_STR}")
            exit(1)

        notification_type = sys.argv[3]
        if notification_type == 'm':
            notify_all_users(is_morning=True)
        elif notification_type == 'e':
            notify_all_users(is_morning=False)
        else:
            print(f"Invalid params. Usage: {USAGE_STR}")
            exit(1)
