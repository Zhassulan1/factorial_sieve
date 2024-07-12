import logging
import telebot
import requests

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Вставьте ваш токен от BotFather
API_TOKEN = '6926589530:AAEDPDIns1Z3IzmftES26tOOey6Mg6pM2D8'
bot = telebot.TeleBot(API_TOKEN)

# Функция старта бота
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("Evaluate Applicants", callback_data='evaluate'))
    markup.row(telebot.types.InlineKeyboardButton("Notify Applicants", callback_data='notify'))
    bot.send_message(message.chat.id, 'Please choose an action:', reply_markup=markup)

# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    if call.data == 'evaluate':
        try:
            response = requests.get('http://127.0.0.1:8000/api/evaluate-applicants/')
            response.raise_for_status()
            bot.answer_callback_query(call.id, "Evaluation request sent successfully.")
        except requests.RequestException as e:
            logger.error(f'Evaluation request error: {e}')
            bot.answer_callback_query(call.id, f"Failed to send evaluation request.")

    elif call.data == 'notify':
        try:
            response = requests.get('http://127.0.0.1:8000/api/notify_all_applicants/')
            response.raise_for_status()
            bot.answer_callback_query(call.id, "Notification request sent successfully.")
        except requests.RequestException as e:
            logger.error(f'Notification request error: {e}')
            bot.answer_callback_query(call.id, f"Failed to send notification request.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text

    api_url = 'https://api.example.com/data'
    params = {'query': user_query}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        result = data.get('result', 'No data available for your query.')
        bot.reply_to(message, result)
    except requests.RequestException as e:
        logger.error(f'Request error: {e}')
        bot.reply_to(message, 'Error occurred while processing your request.')

# Запуск бота
bot.polling(none_stop=True, timeout=60)
