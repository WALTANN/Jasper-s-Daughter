import json
import os
import speech_recognition as sr
import pyttsx3
import random

# Подключаем файл с данными
filename = "users.json"

# Функция загрузки данных пользователей с бд
def load_users(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}
        
# Функция для аутентификации пользователя в ГП
def authenticate(users, login, password):
    for user_id, user_info in users.items():
        if user_info['login'] == login and user_info['password'] == password:
            return user_id
    return None

def main():
    users = load_users(filename)

    # Запрос логина и пароля
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")

    # Проверка данных
    user_id = authenticate(users, login, password)
    if user_id:
        print("Авторизация успешна. Голосовой помощник активирован.")
        recognizer = sr.Recognizer()
        
        while True:
            try:
                with sr.Microphone() as source:
                    print("Скажите что-нибудь...")
                    audio = recognizer.listen(source)

                    # Используем Google Web Speech API для распознавания
                    text = recognizer.recognize_google(audio, language="ru-RU")
                    print(f"Вы сказали: {text}")

                    if text.lower() == "выход":
                        print("Завершение работы голосового помощника.")
                        break
                    elif text.lower() == "привет":
                        responses = ["Привет!", "Приветствую!", "Здравствуйте!"]
                        response = random.choice(responses)
                        print(response)
    else:
        print("Неверный логин или пароль. Пожалуйста, зарегистрируйтесь через телеграм-бота.")

if __name__ == "__main__":
    main()
