from aiogram.utils.keyboard import InlineKeyboardBuilder

def FAQ():
    builder = InlineKeyboardBuilder()
    builder.button(
        text= "1.1	Как работать в Википедии?",
        url= "https://ru.wikipedia.org/wiki/Справка:Введение"
        ),
    builder.button(
        text= "1.2 Как понять язык википедистов?",
        url= "https://ru.wikipedia.org/wiki/Википедия:Глоссарий"
        )
    builder.button(
        text= "1.3	А здесь есть модераторы?",
        url= "https://ru.wikipedia.org/wiki/Википедия:ЧАВО#А_здесь_есть_модераторы?"
        )
    builder.button(
        text= "1.4	Можно скачать всю Википедию?",
        url= "https://ru.wikipedia.org/wiki/Википедия:ЧАВО#Как_понять_язык_википедистов?е"
        )
    builder.button(
        text= "1.5	Короткие ссылки",
        url= "https://ru.wikipedia.org/wiki/Справка:Введение"
        )
    return builder.adjust(1).as_markup()
