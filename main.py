import asyncio
import os
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# храним время последнего сообщения
cooldowns = {}

# кнопка
keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📩 Написать в поддержку")]],
    resize_keyboard=True
)

# команда старт
@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(
        "Привет! Если у тебя есть идея или проблема — напиши нам 👇",
        reply_markup=keyboard
    )

# нажатие кнопки
@dp.message(F.text == "📩 Написать в поддержку")
async def support_start(message: types.Message):
    await message.answer(
        "✉️ Опишите вашу проблему или идею как можно подробнее.\n\n"
        "Если хотите попасть в канал, укажите, как вас отметить (например: @username).\n"
        "Можно оставить сообщение анонимным."
    )

# обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    current_time = time.time()

    # проверка КД (30 минут = 1800 сек)
    if user_id in cooldowns:
        if current_time - cooldowns[user_id] < 1800:
            await message.answer("⏳ Вы уже отправляли сообщение недавно.\nПопробуйте снова через 30 минут.")
            return

    # сохраняем время
    cooldowns[user_id] = current_time

    username = message.from_user.username
    username_text = f"@{username}" if username else "Без username"

    # отправка админу
    await bot.send_message(
        ADMIN_ID,
        f"📩 Новое сообщение:\n\n"
        f"👤 {username_text}\n"
        f"✉️ {message.text}"
    )

    # ответ пользователю
    await message.answer(
        "✅ Сообщение отправлено на модерацию.\nМы обязательно его рассмотрим!"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
