import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from settings import ENDPOINT, HOMEWORK_STATUSES, RETRY_TIME

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s'
)
handler.setFormatter(formatter)


def send_message(bot, message):
    """Отправка сообщения в TELEGRAM."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info('Сообщение отправлено в Telegram')
    except telegram.TelegramError as error:
        logger.error(f'Сбой при отправке сообщения в Telegram: {error}')


def get_api_answer(current_timestamp):
    """Запрос к API сервису Практикума."""
    try:
        current_timestamp = current_timestamp or int(time.time())
        params = {'from_date': current_timestamp}
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            message = f'ошибочный статус ответа API: {response.status_code}'
            logger.error(message, exc_info=True)
            raise ConnectionError(message)
    except Exception as error:
        message = f'Запрос не удался: {error}'
        logger.error(message)
        raise ValueError(message)
    return response.json()


def check_response(response):
    """Проверка ответа API на корректность."""
    if not isinstance(response, dict):
        message = 'Неверный тип данных'
        raise TypeError(message)
    if 'homeworks' not in response:
        message = 'Ключ homeworks отсутствует'
        raise KeyError(message)
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        message = 'Неверный тип данных'
        raise TypeError(message)
    if not homeworks:
        message = 'Список homework пуст'
        raise ValueError(message)
    homework = response['homeworks'][0]
    return homework


def parse_status(homework):
    """Извлекаем название и статус домашней работы."""
    if 'homework_name' not in homework:
        message = 'Ключ homework_name отсутствует'
        raise KeyError(message)
    homework_name = homework['homework_name']
    if 'status' not in homework:
        message = 'Ключ status отсутствует'
        raise KeyError(message)
    homework_status = homework['status']
    if not isinstance(homework_name, str):
        message = 'Неверный тип данных homework_name'
        raise TypeError(message)
    if not isinstance(homework_status, str):
        message = 'Неверный тип данных homework_status'
        raise TypeError(message)
    if homework_status in HOMEWORK_STATUSES:
        verdict = HOMEWORK_STATUSES[homework_status]
    else:
        message = (f'Неизвестный статус домашней работы: {homework_status}')
        raise KeyError(message)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка Токенов."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        message = 'Необходимые переменные окружения отсутствуют.'
        logger.critical(message, exc_info=True)
        sys.exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    try:
        response = get_api_answer(current_timestamp)
        homework = check_response(response)
        message = parse_status(homework)
        send_message(bot, message)
        time.sleep(RETRY_TIME)
    except Exception as error:
        message = f'Сбой в работе программы: {error}'
    finally:
        send_message(bot, message)
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
