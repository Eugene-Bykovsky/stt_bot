import requests
from config import FOLDER_ID, IAM_TOKEN


def speech_to_text(data):
    # указываем параметры запроса
    params = "&".join([
        "topic=general",  # используем основную версию модели
        f"folderId={FOLDER_ID}",
        "lang=ru-RU"  # распознаём голосовое сообщение на русском языке
    ])
    url = f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}"
    # аутентификация через IAM-токен
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }
    # выполняем запрос
    response = requests.post(url=url, headers=headers, data=data)
    # преобразуем json в словарь
    decoded_data = response.json()
    # проверяем не произошла-ли ошибка при запросе
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get(
            "result")  # возвращаем статус и текст из аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"  # возвращаем статус и сообщение об ошибке
