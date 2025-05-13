from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Хранилище подписок (в реальности — база)
user_subscriptions = {}

# Старт
# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Это Ксю и мои медитации")
    
    # Открываем и отправляем видео
    with open("Hi_video.mp4") as video:
        await update.message.reply_video(video=video)

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
    TOKEN = "7856590549:AAFoX1l5TB7xhxMBtcQ5gh9yOhWr4bjhuOw"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meditation", meditation))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == '__main__':
    main()
