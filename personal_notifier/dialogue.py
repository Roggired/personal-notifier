from personal_notifier.model.user import User


def get_ready_appeal(
    user: User
) -> str:
    raw_appeal: str = (user.nickname if user.nickname != '' else user.name).strip()
    if raw_appeal != '':
        ready_appeal = raw_appeal.lower()
        ready_appeal = ready_appeal[0].upper() + ready_appeal[1:]
        return ready_appeal

    return raw_appeal


def get_answer(
    user: User,
    message: str
) -> str:
    ready_appeal: str = get_ready_appeal(user)

    if ready_appeal != '':
        return f"{ready_appeal}, вместо того чтобы болтать со мной, иди и заполни time-management!"

    return "Не знаю, как звать тебя, но вместо того чтобы болтать со мной, иди и заполни time-management!"


def already_registered_message(
    user: User
) -> str:
    ready_appeal: str = get_ready_appeal(user)
    if ready_appeal != '':
        return f"Хей, {ready_appeal}, ты уже зарегистрирован, поэтому иди и заполни time-management"
    return f"Хей, ты уже зарегистрирован, поэтому иди и заполни time-management"


def new_user_message(
    user: User
) -> str:
    ready_appeal: str = get_ready_appeal(user)
    if ready_appeal != '':
        return f"Приветствую, {ready_appeal}! Я твой личный напоминальщик про time-management. Поэтому иди и заполни его!"

    return "Приветствую! Я твой личный напоминальщик про time-management. Поэтому иди и заполни его!"


def bye_existed_user_message(
    user: User
) -> str:
    ready_appeal: str = get_ready_appeal(user)
    if ready_appeal != '':
        return f"{ready_appeal}, значит ты научился самостоятельно вести time-management? Молодец! Таков путь."

    return "Значит ты научился самостоятельно вести time-management? Молодец! Таков путь."


def bye_not_found_user_message(
    user: User
) -> str:
    return "Прежде чем отписываться от меня, сперва зарегистрируйся! Иначе как я буду тебя учить заполнять time-management?"


def morning_notification(
    user: User
) -> str:
    ready_appeal: str = get_ready_appeal(user)
    if ready_appeal != '':
        return f"Доброе утро, {ready_appeal}!\nНадеюсь, ты прилежно ведешь time-mangement! Если нет - не забудь заполнить его"

    return "Доброе утро!\nНадеюсь, ты прилежно ведешь time-mangement! Если нет - не забудь заполнить его"


def evening_notification(
    user: User
) -> str:
    ready_appeal: str = get_ready_appeal(user)
    if ready_appeal != '':
        return f"{ready_appeal}, ура! Близится конец очередного рабочего дня!\nЯ надеюсь, ты заполнил time-management?"

    return "Ура! Близится конец очередного рабочего дня!\nЯ надеюсь, ты заполнил time-management?"
