from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import datetime

from config import *
from state import *
import app.database.requests as rq
import app.keyboard as kb

user_router = Router()

bot = Bot(token=TOKEN_TG)
dp = Dispatcher()

count_photo = 0


# срочно
@user_router.message(Command("add_filter"))
async def cmd_add_filter(message: Message, state: FSMContext):
    global count,count_photo
    count_photo = 0
    count = 0
    global id
    tg_id = await rq.get_id(message.from_user.id)
    print(tg_id)
    if tg_id in id:
        await message.answer("Напишите слово, которое хотите добавить в фильтр")
        await state.set_state(waiting.add_a_word_to_filter)
    else:
        await message.answer("Вы не админ!")

@user_router.message(waiting.add_a_word_to_filter)
async def add_word_to_filer(message: Message, state: FSMContext):
    keywords = ["важно", "требуется", message.photo[-1].file_id]
    message_update = message.text

    if message_update.startswith('/'):
        await message.reply(
            "Команда не может быть добавлена в список фильтров.\nПожалуйста, если вы хотите выйти из функции /add_filter, напишите команду, которую хотите использовать, либо зайдите в функию заново, чтобы добавить фильтр!"
        )
        await state.clear()
        return

    if message_update:
        message_update = message_update.lower()
    elif not message_update:
        await message.reply("Сообщений нет, которые можно добавить в фильтр! ")

    keywords.append(message_update)
    print(f"Фильтр: {keywords}")
    await message.answer(f"Фильтр: {', '.join(keywords)}")

@user_router.message(Command("delete_filter"))
async def cmd_delete_filter(message: Message, state: FSMContext):
    global count,count_photo
    count_photo = 0
    count = 0
    global id
    tg_id = await rq.get_id(message.from_user.id)

    if tg_id in id:
        await message.answer("Напишите слово, которое хотите удалить из фильтра")
        await state.set_state(waiting.delete_a_word_from_filter)
    else:
        await message.answer("Вы не админ!")

@user_router.message(waiting.delete_a_word_from_filter)
async def delete_word_from_filter(message: Message, state: FSMContext):
    global keywords
    message_update = message.text

    if message_update.startswith('/'):
        await message.reply(
            "Команда не может быть добавлена в список фильтров.\nПожалуйста, если вы хотите выйти из функции /delete_filter, напишите команду, которую хотите использовать, либо зайдите в функцию заново, чтобы добавить фильтр!"
        )
        await state.clear()
        return

    if message_update:
        message_update = message_update.lower()

        # Удаляем слово из фильтра, если оно существует
        if message_update in keywords:
            keywords.remove(message_update)
            await message.answer(f"Слово '{message_update}' удалено из фильтра.")
        else:
            await message.answer(f"Слово '{message_update}' не найдено в фильтре.")
    else:
        await message.reply("Сообщений нет, которые можно удалить из фильтра!")

    print(f"Фильтр: {keywords}")

@user_router.message(Command("change"))
async def change_channel(message: Message, state: FSMContext):
    global count_photo,count
    count = 0
    count_photo = 0
    global id
    tg_id = await rq.get_id(message.from_user.id)
    print(tg_id)
    text1 = "Вы не админ!"
    if tg_id in id:
        await message.answer("Напиши тг канал куда, будут отправляться сообщения ")
        await state.set_state(waiting.waiting_a_group)
    else:
        await message.reply(text=text1)

@user_router.message(waiting.waiting_a_group)
async def change_id_group(message: Message, state: FSMContext):
    await state.clear()
    message_update = message.text
    try:
        if not message_update.startswith('@'):
            await message.answer("Название канала должно начинаться с \"@\" ")
        else:
            # Проверка на существование канала
            try:
                chat = await bot.get_chat(message_update)
                await rq.set_group(message.from_user.id, message_update)
                await message.answer("Группа успешно занесена в бд")
            except Exception as e:
                await message.answer("Канал не существует или бот не имеет доступа к нему.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@user_router.message(Command("help"))
async def cmd_help(message: Message):
    global id
    tg_id = await rq.get_id(message.from_user.id)
    global count, count_photo
    count_photo = 0
    count = 0
    print(tg_id)
    if tg_id in id:
        await message.reply(text=
                            "<b>Привет! Это бот для отправления сообщений из одного чата в другой.\nДоступные команды для админа:</b>\n"
                            "/start - Запустить работу\n"
                            "/help - помощь в работе с ботом\n"
                            "/admin - админ-панель\n"
                            "/questions - FAQ",
                            parse_mode="HTML"
                            )
    else:
        await message.reply(text=
                            "<b>Привет! Это бот для отправления сообщений из одного чата в другой.\nДоступные команды для обычного юзера:</b>\n"
                            "/start - Запустить работу\n"
                            "/help - помощь в работе с ботом\n"
                            "/questions - FAQ",
                            parse_mode="HTML"
                            )

@user_router.message(Command("admin"))
async def cmd_admin(message: Message):
    tg_id = await rq.get_id(message.from_user.id)
    print(tg_id)
    text = "Доступные команды для админа:\n/send_message - отправить сообщение в другой чат\n/add_filter - добавить фильр\n/delete_filter - удалить фильтр\n/change - изменить канал\n\n"
    text1 = "Вы не администратор!"
    if tg_id in id:
        global count,count_photo
        count_photo = 0
        count = 0
        await message.answer(text=text, parse_mode="HTML")
    else:
        await message.reply(text=text1)

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    global count,count_photo
    count_photo = 0
    count = 0
    await rq.set_datas(message.from_user.id, message.from_user.full_name)
    text = "Привет! Я твой бот-помощник в отправлении сообщений из одного чата в другой\nНапиши команду /send_message, для того чтобы, отправить нужное сообщения, сколько тебе нужно."
    await message.answer(text=text)

@user_router.message(Command("send_message"))
async def cmd_send_message(message: Message, state: FSMContext):
    global id
    text = "Напиши любое сообщение для пересылки его в другой канал(Напиши \"стоп\", если хочешь прекратить работу):"
    text1 = "Вы не администратор!"
    tg_id = await rq.get_id(message.from_user.id)
    print(tg_id)

    if tg_id in id:
        global count,count_photo
        count_photo = 0
        count = 0
        await message.reply(text=text)
        await state.set_state(waiting.waiting_a_message)
    else:
        await message.reply(text=text1)

@user_router.message(waiting.waiting_a_message)
async def send_message(message: Message, state: FSMContext):
    global count,count_photo
    keywords = ["важно", "требуется"]
    message_update = message.text
    current_time = datetime.datetime.now().strftime("%d.%m.%Y, %H:%M")
    chat_2 = await rq.get_group(message.from_user.id)
    print(f"Channel: {chat_2}")

    if message_update and message_update.lower() == 'стоп':
        await cmd_stop(message)
        await state.clear()
        return

    message_type = "Сообщение" if message.text else "Изображение"

    if message_update and any(keyword in message_update.lower() for keyword in keywords):
        count += 1
        await message.answer(
            f"Время отправки: <b>{current_time}</b>\nСообщение отправлено от: {message.from_user.id}\nТип сообщения: {message_type}\nТекст: {message_update}\n<b>Статус отправки: Корректно</b>",
            parse_mode="HTML"
        )
        await message.answer(f"<b>Сообщений отправлено: {count}</b>✅", parse_mode="HTML")
        await notify_user(message, message_update)
        await bot.send_message(chat_id=chat_2, text=message_update)
    elif message.photo:
        pass
    else:
        await message.answer(
            f"Время отправки: {current_time}\nТип сообщения: {message_type}\nТекст: {message_update}\nСообщение отправлено от: {message.from_user.id}\nСтатус отправки: Ошибка"
        )
        await message.answer("Сообщение не соответствует критериям фильтрации и не было отправлено.")

    if message.photo:
        count_photo += 1
        photo = message.photo[-1].file_id
        await bot.send_photo(chat_id=chat_2, photo=photo, caption=message_update)
        await message.answer(f"<b>Изображений отправлено: {count_photo}</b>✅", parse_mode="HTML")
        await message.answer(
            f"Время отправки: <b>{current_time}</b>\nСообщение отправлено от: {message.from_user.id}\nТип сообщения: {message_type}\nТекст: {message_update}\n<b>Статус отправки: Корректно</b>",
            parse_mode="HTML"
        )
        await notify_user(message, message_update)
    else:
        pass

async def notify_user(message:Message, message_text: str):
    if message.text:
        await message.answer(text=f"Ваше сообщение было успешно переслано: <b>{message_text}</b>",parse_mode="HTML")
    else:
        await message.answer(text=f"Ваше фото было успешно отправлено", parse_mode="HTML")

async def questions(message: Message):
    global count,count_photo
    count_photo = 0
    count = 0
    await message.answer("Ответы на часто задаваемые вопросы про википедию", reply_markup=kb.FAQ())

@user_router.message(F.text == "стоп")
async def cmd_stop(message: Message):
    global count,count_photo
    count_photo = 0
    count = 0
    await message.answer("Вы остановили процесс")

# @user_router.message()
# async def cmd_exist(message:Message):
#     global count
#     count = 0
#     await message.answer("Неизвестная команада.")