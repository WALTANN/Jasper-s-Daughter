import json
import os
import speech_recognition as sr
import pyttsx3


# Подключаем файл с данными
filename = "users.json"

# Функция загрузки данных пользователей с бд
def load_users(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}
