import math

from config import MAX_USER_STT_BLOCKS


def is_stt_block_limit(user_id, duration, db):
    audio_blocks = math.ceil(
        duration / 15)  # переводим секунды в аудиоблоки и округляем в большую сторону
    # функция из БД для подсчёта всех потраченных пользователем аудиоблоков
    if not db.count_all_blocks('stt_blocks', user_id):
        all_blocks = audio_blocks
    else:
        all_blocks = db.count_all_blocks('stt_blocks', user_id) + audio_blocks

    # проверяем, что аудио длится меньше 30 секунд
    if duration >= 30:
        return None, "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"

    # сравниваем all_blocks с количеством доступных пользователю аудиоблоков
    if all_blocks > MAX_USER_STT_BLOCKS:
        return None, f"Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}"

    # если всё ок - возвращаем размер этого голосового сообщения
    return audio_blocks, ""
