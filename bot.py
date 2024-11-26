from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random

# Словарь для хранения состояния каждого пользователя
user_data = {}

# Функция для старта
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'electricity': 0, 'level': 1}
    
    update.message.reply_text(f"Привет, {update.message.from_user.first_name}! Я Voltis. Нажимай на меня, чтобы получить электричество! Текущий уровень: {user_data[user_id]['level']}")

# Функция для получения электричества
def get_electricity(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'electricity': 0, 'level': 1}
    
    # Увеличиваем количество электричества
    electricity_gain = random.randint(1, 3) * user_data[user_id]['level']
    user_data[user_id]['electricity'] += electricity_gain
    
    update.message.reply_text(f"Ты получил {electricity_gain} единиц электричества! Всего у тебя: {user_data[user_id]['electricity']} электричества.")

# Функция для улучшения уровня
def upgrade(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'electricity': 0, 'level': 1}
    
    cost = user_data[user_id]['level'] * 10  # Стоимость повышения уровня
    
    if user_data[user_id]['electricity'] >= cost:
        user_data[user_id]['electricity'] -= cost
        user_data[user_id]['level'] += 1
        update.message.reply_text(f"Поздравляю! Ты улучшил уровень! Новый уровень: {user_data[user_id]['level']}. Остаток электричества: {user_data[user_id]['electricity']}")
    else:
        update.message.reply_text(f"У тебя недостаточно электричества для улучшения. Нужно {cost} электричества, а у тебя только {user_data[user_id]['electricity']}.")

# Основная функция
def main() -> None:
    # Voltis Coin
    token = "ВАШ_ТЕГ_Бота_ЗДЕСЬ"
    
    updater = Updater(token)
    
    dispatcher = updater.dispatcher

    # Обработчик команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("upgrade", upgrade))

    # Обработчик нажатия на сообщения
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_electricity))

    # Запуск бота
    updater.start_polling()

    # Ожидание завершения
    updater.idle()

if __name__ == '__main__':
    main()
