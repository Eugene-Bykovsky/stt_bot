import logging
from telebot import TeleBot

from config import TELEGRAM_TOKEN
from speechkit import speech_to_text
from database import Database
from utils import is_stt_block_limit

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename='logs.log',
    filemode="a",
    datefmt="%Y-%m-%d %H:%M:%S"
)

bot = TeleBot(TELEGRAM_TOKEN)

db = Database()
db.create_table()


# Обрабатываем команду /stt
@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id,
                     'Отправь голосовое сообщение, чтобы я его распознал!')
    bot.register_next_step_handler(message, stt)


# Переводим голосовое сообщение в текст после команды stt
def stt(message):
    user_id = message.from_user.id

    # Проверка, что сообщение действительно голосовое
    if not message.voice:
        print('Это не голос')
        bot.send_message(user_id,
                         'Вы прислали текст, нужно голосовое сообщение!')
        return

    # Считаем аудиоблоки и проверяем сумму потраченных аудиоблоков
    stt_blocks, error_message = is_stt_block_limit(user_id,
                                                   message.voice.duration, db)

    if not stt_blocks:
        bot.send_message(user_id, error_message)
        return

    file_id = message.voice.file_id  # получаем id голосового сообщения
    file_info = bot.get_file(
        file_id)  # получаем информацию о голосовом сообщении
    file = bot.download_file(
        file_info.file_path)  # скачиваем голосовое сообщение

    # Получаем статус и содержимое ответа от SpeechKit
    status, text = speech_to_text(
        file)  # преобразовываем голосовое сообщение в текст

    print(status, text)

    # Если статус True - отправляем текст сообщения и сохраняем в БД,
    # иначе - сообщение об ошибке
    if status:
        # Записываем сообщение и кол-во аудиоблоков в БД
        db.insert_row(user_id, text, 'stt_blocks', stt_blocks)
        bot.send_message(user_id, text, reply_to_message_id=message.id)
    else:
        bot.send_message(user_id, text)


bot.polling()
