import json
import os
import speech_recognition as sr
import pyttsx3
import random
from datetime import datetime, timedelta
import webbrowser

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

# Функция для получения текущего времени в часовом поясе UTC+3
def get_current_time_utc_plus_3():
    current_time = datetime.utcnow() + timedelta(hours=3)
    return current_time.strftime("%H:%M:%S")
    
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
                    elif text.lower() == "время":
                        current_time = get_current_time_utc_plus_3()
                        response = f"{current_time}"
                        print(response)
                    elif text.lower() == "привет":
                        responses = ["Привет!", "Приветствую!", "Здравствуйте!"]
                        response = random.choice(responses)
                        print(response)
                    elif text.lower() == "random":
                        random_number = random.randint(0, 10)
                        response = f"Случайное число: {random_number}"
                        print(response)      
                    elif text.lower() == "открой настройки":
                        os.system("control")
                        response = "Открываю настройки."
                        print(response)     
                    elif text.lower() == "открой калькулятор":
                        os.system("calc")
                        response = "Открываю калькулятор."
                        print(response)
                    elif text.lower() == "открой браузер":
                        webbrowser.open("http://www.ya.ru")
                        response = "Открываю браузер."
                        print(response)
                    else:
                        user_commands = users[user_id].get('commands', [])
                        command_found = False
                        for command in user_commands:
                            if text.lower() == command['name'].lower():
                                webbrowser.open(command['url'])
                                response = "Открываю"
                                print(response)
                                
                                command_found = True
                                break
                        if not command_found:
                            response = "Команда не распознана."
                            print(response)
            except sr.UnknownValueError:
                print("Не удалось распознать речь.")
                
            except sr.RequestError as e:
                print(f"Ошибка сервиса распознавания речи; {e}")
    else:
        print("Неверный логин или пароль. Пожалуйста, зарегистрируйтесь через телеграм-бота.")

if __name__ == "__main__":
    main()
