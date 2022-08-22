# Homework_bot

# Описание:
Telegram-бот, который обращается к API сервису Практикум.Домашка и узнает статус домашней работы пользователя: взято ли его домашнее задание в ревью, проверено ли оно, а если проверено —  принял ли его ревьюер или вернул на доработку. В случае наличия изменений в статусе домашней работы бот присылает соответствующее уведомление в Telegram.

# Стек технологий:
Python, Python-telegram-bot

# Установка:

Клонировать репозиторий и перейти в него в командной строке: git clone https://@github.com/comdastim/homework_bot.git

cd homework_bot

Cоздать виртуальное окружение: python3 -m venv env

Активировать виртуальное окружение: source env/bin/activate(для macOS или Linux:) либо source/venv/Scripts/activate (для Windows)

Установить зависимости из файла requirements.txt: python3 -m pip install --upgrade pip pip install -r requirements.txt

Выполнить миграции: python3 manage.py migrate

Запустить проект: python3 manage.py runserver

# Авторы:

Дарья Тимохина
