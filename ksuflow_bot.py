import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Хранилище подписок (в реальности — база)
user_subscriptions = {}

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Попробовать медитацию", callback_data='try')],
        [InlineKeyboardButton("Оформить подписку", callback_data='subscribe')],
        [InlineKeyboardButton("Что внутри?", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот для медитаций. Чем займёмся?", reply_markup=reply_markup)

    # Отправка видео Hi_video.mp4 при старте
    try:
        with open("Hi_video.mp4", "rb") as video:
            await update.message.reply_video(video=video, caption="Добро пожаловать! Вот видео-приветствие")
    except FileNotFoundError:
        await update.message.reply_text("Видео Hi_video.mp4 не найдено.")

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'try':
        await query.message.reply_audio(audio=open('sample_meditation.mp3', 'rb'),
                                        caption="Вот пробная медитация. Готов(а) ко всей библиотеке?")
    elif query.data == 'info':
        await query.message.reply_text("У нас есть медитации на тревогу, сон, бодрость, любовь к себе и другие.")
    elif query.data == 'subscribe':
        user_subscriptions[user_id] = True  # Здесь должна быть реальная проверка оплаты
        await query.message.reply_text("Подписка оформлена! Теперь у тебя есть доступ ко всем медитациям.")
    elif query.data == 'premium':
        if user_subscriptions.get(user_id):
            await query.message.reply_audio(audio=open('full_meditation.mp3', 'rb'),
                                            caption="Вот твоя сегодняшняя медитация.")
        else:
            await query.message.reply_text("Эта функция доступна только по подписке.")

# Команда для доступа к медитации
async def meditation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_subscriptions.get(user_id):
        await update.message.reply_audio(audio=open('full_meditation.mp3', 'rb'),
                                         caption="Вот твоя медитация на сегодня.")
    else:
        await update.message.reply_text("Оформи подписку, чтобы получить доступ.")

# Запуск

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meditation", meditation))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == '__main__':
    main()
