from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import datetime

from config import TOKEN_TG,id
from state import waiting
import app.database.requests as rq
import app.keyboard as kb

user_router = Router()

bot = Bot(token=TOKEN_TG)
dp = Dispatcher()

keywords = []
count_photo = 0

@user_router.message(Command('see_filter'))
async def see_filter(message: Message):
    global keywords
    if not keywords:
        await message.answer("В фильтре нет слов")
        return
    keywords_str = ', '.join(keywords)
    await message.answer(f"Твой фильтр: {keywords_str}")

@user_router.message(Command("add_filter"))
async def cmd_add_filter(message: Message, state: FSMContext):
    tg_id = await rq.get_id(message.from_user.id)
    if tg_id in id:
        await message.answer("Напишите слово, которое хотите добавить в фильтр")
        await state.set_state(waiting.add_a_word_to_filter)
    else:
        await message.answer("Вы не админ!")

@user_router.message(waiting.add_a_word_to_filter)
async def add_word_to_filter(message: Message, state: FSMContext):
    global keywords
    message_update = message.text.lower()
    if message_update.startswith('/'):
        await message.reply(
            "Команда не может быть добавлена в список фильтров.\nПожалуйста, если вы хотите выйти из функции /add_filter, напишите команду, которую хотите использовать, либо зайдите в функцию заново, чтобы добавить фильтр!"
        )
        await state.clear()
        return
    keywords.append(message_update)
    await message.answer(f"Фильтр: {', '.join(keywords)}")

@user_router.message(Command("delete_filter"))
async def cmd_delete_filter(message: Message, state: FSMContext):
    tg_id = await rq.get_id(message.from_user.id)
    if tg_id in id:
        await message.answer("Напишите слово, которое хотите удалить из фильтра")
        await state.set_state(waiting.delete_a_word_from_filter)
    else:
        await message.answer("Вы не админ!")

@user_router.message(waiting.delete_a_word_from_filter)
async def delete_word_from_filter(message: Message, state: FSMContext):
    global keywords
    message_update = message.text.lower()
    if message_update.startswith('/'):
        await message.reply(
            "Команда не может быть добавлена в список фильтров.\nПожалуйста, если вы хотите выйти из функции /delete_filter, напишите команду, которую хотите использовать, либо зайдите в функцию заново, чтобы добавить фильтр!"
        )
        await state.clear()
        return
    if message_update in keywords:
        keywords.remove(message_update)
        await message.answer(f"Слово '{message_update}' удалено из фильтра.")
    else:
        await message.answer(f"Слово '{message_update}' не найдено в фильтре.")
    await message.answer(f"Фильтр: {', '.join(keywords)}")

@user_router.message(Command("change"))
async def change_channel(message: Message, state: FSMContext):
    tg_id = await rq.get_id(message.from_user.id)
    if tg_id in id:
        await message.answer("Напиши тг канал куда, будут отправляться сообщения")
        await state.set_state(waiting.waiting_a_group)
    else:
        await message.reply("Вы не админ!")

@user_router.message(waiting.waiting_a_group)
async def change_id_group(message: Message, state: FSMContext):
    await state.clear()
    message_update = message.text
    if not message_update.startswith('@'):
        await message.answer("Название канала должно начинаться с \"@\"")
        return
    try:
        chat = await bot.get_chat(message_update)
        await rq.set_group(message.from_user.id, message_update)
        await message.answer("Группа успешно занесена в базу данных")
    except Exception:
        await message.answer("Канал не существует или бот не имеет доступа к нему.")

@user_router.message(Command("help"))
async def cmd_help(message: Message):
    tg_id = await rq.get_id(message.from_user.id)
    if tg_id in id:
        await message.reply(
            "<b>Привет! Это бот для отправления сообщений из одного чата в другой.\nДоступные команды для админа:</b>\n"
            "/start - Запустить работу\n"
            "/help - помощь в работе с ботом\n"
            "/admin - админ-панель\n"
            "/questions - FAQ",
            parse_mode="HTML"
        )
    else:
        await message.reply(
            "<b>Привет! Это бот для отправления сообщений из одного чата в другой.\nДоступные команды для обычного юзера:</b>\n"
            "/start - Запустить работу\n"
            "/help - помощь в работе с ботом\n"
            "/questions - FAQ",
            parse_mode="HTML"
        )

@user_router.message(Command("admin"))
async def cmd_admin(message: Message):
    tg_id = await rq.get_id(message.from_user.id)
    if tg_id in id:
        await message.answer(
            "Доступные команды для админа:\n"
            "/send_message - отправить сообщение в другой чат\n"
            "/add_filter - добавить фильтр\n"
            "/delete_filter - удалить фильтр\n"
            "/change - изменить канал или добавить его\n"
            "/see_filter - посмотреть фильтр слов\n",
            parse_mode="HTML"
        )
    else:
        await message.reply("Вы не администратор!")

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_datas(message.from_user.id, message.from_user.full_name)
    await message.answer(
        "Привет! Я твой бот-помощник в отправлении сообщений из одного чата в другой\n"
        "Напиши команду /send_message, для того чтобы, отправить нужное сообщения,"
        "сколько тебе нужно."
    )

@user_router.message(Command("send_message"))
async def cmd_send_message(message: Message, state: FSMContext):
    tg_id = await rq.get_id(message.from_user.id)
    if tg_id in id:
        await message.reply(
            "Напиши любое сообщение или отправь фото для пересылки его в другой канал"
            "(Напиши \"стоп\", если хочешь прекратить работу):"
            )
        await state.set_state(waiting.waiting_a_message)
    else:
        await message.reply("Вы не администратор!")

@user_router.message(waiting.waiting_a_message)
async def send_message(message: Message, state: FSMContext):
    global keywords
    message_update = message.text
    current_time = datetime.datetime.now().strftime("%d.%m.%Y, %H:%M")
    chat_2 = await rq.get_group(message.from_user.id)

    if not chat_2:
        await message.answer("Не добавлен чат в базу данных")
        await state.clear()
        return

    if message_update and message_update.lower() == 'стоп':
        await cmd_stop(message)
        await state.clear()
        return

    if message_update and any(keyword in message_update.lower() for keyword in keywords):
        await bot.send_message(chat_id=chat_2, text=message_update)
        await notify_user(message, message_update, current_time, "Сообщение")
    elif message.photo:
        photo = message.photo[-1].file_id
        await bot.send_photo(chat_id=chat_2, photo=photo, caption=message_update)
        await notify_user(message, message_update, current_time, "Изображение")
    else:
        await message.answer(
            "Сообщение не соответствует критериям фильтрации и не было отправлено."
            )

async def notify_user(message: Message, message_text: str, current_time: str, message_type: str):
    await message.answer(
        f"Время отправки: <b>{current_time}</b>\n"
        f"Сообщение отправлено от: {message.from_user.id}\n"
        f"Тип сообщения: {message_type}\n"
        f"Текст: {message_text}\n"
        f"<b>Статус отправки: Корректно</b>",
        parse_mode="HTML"
    )

@user_router.message(Command("questions"))
async def questions(message: Message):
    await message.answer("Ответы на часто задаваемые вопросы про википедию", reply_markup=kb.FAQ())

@user_router.message(F.text == "стоп")
async def cmd_stop(message: Message):
    await message.answer("Вы остановили процесс")
