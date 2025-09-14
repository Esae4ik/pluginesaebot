import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def start(update, context):
    update.message.reply_text("Привет! Используй команду:\n/plugin <имя> <код>")

def create_plugin(update, context):
    if len(context.args) < 2:
        update.message.reply_text("Формат: /plugin <имя> <код>")
        return

    name = context.args[0].strip()
    code = ' '.join(context.args[1:]).strip()

    if not name.isidentifier():
        update.message.reply_text("Недопустимое имя файла.")
        return

    filename = f"{name}.plugin"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)

        update.message.reply_text(f"Файл {filename} создан.")
        with open(filename, 'rb') as f:
            update.message.reply_document(f)

    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def echo(update, context):
    update.message.reply_text("Используй команду:\n/plugin <имя> <код>")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("plugin", create_plugin))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    print("Бот запущен...")
    updater.idle()

if __name__ == '__main__':
    main()
