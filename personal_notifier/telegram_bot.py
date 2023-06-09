from typing import List, Tuple, Callable, Optional

from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from personal_notifier.dialogue import get_answer, \
    already_registered_message, \
    new_user_message, \
    bye_existed_user_message, \
    bye_not_found_user_message
from personal_notifier.envs import TELEGRAM_BOT_TOKEN_ENV_VARIABLE, get_env
from personal_notifier.model.user import User
from personal_notifier.storage.json_file_storage import JsonFileStorage


def _update_to_user(
    update: Update
) -> User:
    return User(
        id=update.message.chat_id,
        name=update.message.chat.first_name,
        nickname=''
    )


def _search_author_user_template(
    update: Update,
    func: Optional[Callable[[bool, int, User, List[User], JsonFileStorage], None]]
) -> Tuple[bool, User]:
    author_user: User = _update_to_user(update)
    json_file_storage: JsonFileStorage = JsonFileStorage.default()
    all_users = json_file_storage.load_users()

    is_user_found: bool = False
    user_index: int = -1
    for i in range(len(all_users)):
        user = all_users[i]
        if user.id == author_user.id:
            is_user_found = True
            user_index = i

    if func:
        func(is_user_found, user_index, author_user, all_users, json_file_storage)

    return is_user_found, author_user


async def _start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    def _save_user_if_new(
            is_user_found: bool,
            user_index: int,
            author_user: User,
            all_users: List[User],
            json_file_storage: JsonFileStorage
    ) -> None:
        if not is_user_found:
            all_users.append(author_user)
            json_file_storage.save_users(all_users)

    (is_user_found, author_user) = _search_author_user_template(
        update=update,
        func=_save_user_if_new
    )

    if is_user_found:
        await update.message.reply_text(already_registered_message(author_user))
        return

    await update.message.reply_text(new_user_message(author_user))


async def _bye_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    def _remove_user_if_found(
        is_user_found: bool,
        user_index: int,
        author_user: User,
        all_users: List[User],
        json_file_storage: JsonFileStorage
    ) -> None:
        if is_user_found:
            del all_users[user_index]
            json_file_storage.save_users(all_users)

    (is_user_found, author_user) = _search_author_user_template(
        update=update,
        func=_remove_user_if_found
    )

    if is_user_found:
        await update.message.reply_text(bye_existed_user_message(author_user))
        return

    await update.message.reply_text(bye_not_found_user_message(author_user))


async def _random_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    author_user: User = _update_to_user(update)
    all_users: List[User] = JsonFileStorage.default().load_users()

    is_user_found: bool = False
    for user in all_users:
        if user.id == author_user.id:
            is_user_found = True
            break

    if not is_user_found:
        await update.message.reply_text(text="Хто ты, путник? Напиши '/start', чтобы начать")
        return

    answer: str = get_answer(
        user=author_user,
        message=update.message.text
    )
    await update.message.reply_text(answer)


async def notify_about_time_management(
    user: User,
    message: str
) -> None:
    bot = Bot(get_env(TELEGRAM_BOT_TOKEN_ENV_VARIABLE))
    async with bot:
        await bot.send_message(
            text=message,
            chat_id=user.id,
        )


def start_personal_notifier_long_polling_bot() -> None:
    token: str = get_env(TELEGRAM_BOT_TOKEN_ENV_VARIABLE)

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", _start_command_handler))
    application.add_handler(CommandHandler("bye", _bye_command_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _random_message_handler))

    application.run_polling()
