# Голосовой помощник с использованием телеграм-бота и базы данных

Этот проект представляет собой голосового помощника, который обеспечивает пользователей возможностью управлять своими задачами с помощью голоса. Он включает в себя телеграм-бота для регистрации пользователей и управления их персональными командами, а также голосового помощника, который может выполнять эти команды.


# Основа проекта

## База данных
Используется своя база данных. База данных хранится в директории DB. Данные сохраняются в файле с расширением '.json' (более удобный формат).

*Методы базы данных приведены ниже.*

## Телеграм-бот
Телеграм бот написан на **aiogram**. Использовался данный framework, так как он позволяет работать асинхронно, что снижает нагрузку на телеграм-бота.


## Голосовой помощник
Голосовой помощник написан с помощью speech_recognition, pyttsx3 (более удобные библиотеки для участников проекта). 
*Описание приведено ниже*

# Функциональность

## База данных
База данных имеет ряд методов для работы с информацией, хранящейся в 'filenane.json'
1. **save_data** - сохранение данных в файле
2. **add_user** - добавление пользователя в файл
3. **get_user** - сбор информации о пользователе
4. **update_password** - обновление пароля пользователя 
5. **update_username** - обновление имени пользователя 
6. **add_command** - добавление пользовательской команды 
7. **get_commands** - просмотр пользовательских команд 
8. **delete_command** - удаление пользовательской команды по названию 
9. **delete_user** - удаление пользователя из базы данных
10. **get_all_users** - достать ID и username всех пользователей


## Телеграм-бот
1. **Регистрация и аутентификация пользователей:**
   - Пользователи могут зарегистрироваться, предоставив свое имя, логин и пароль.
   - После регистрации они могут использовать свой логин и пароль для аутентификации в голосовом помощнике.
   
2. **Управление профилем:**
   - Пользователи могут обновлять свой пароль и имя пользователя.
   - Пользователи могут добавлять и удалять команды голосового помощника.

3. **Список команд:**
   3.1 **Регистрация:**
   - отправить команду `/start` для регистрации.

   ### ***После регистрации вы можете:***

   3.2. **Редактировать пароль:**
      - Отправить боту команду `/uppass` для изменения пароля.

   3.3. **Редактировать username:**
      - Отправить боту команду `/upusername` для изменения пароля.
   
   3.4. **Добавлять команды**:
      - Добавить новую команду с помощью команды /newcommand в телеграм-боте.

   3.5. **Удалять команды**:
      - Добавить новую команду с помощью команды /deletecommand в телеграм-боте.
        
   3.6 **Удалить профиль:**
      - Введите команду `/deleteprofile` и профиль удалиться из базы данных.

   3.7. **Использование голосового помощника:**
      - После регистрации и добавления команд вы можете использовать голосовой помощник для выполнения этих команд, произнося их названия.

   ### ***Команда админа:***

   3.8 **Посмотреть пользователей:**
      - Введите команду `/checkusers` и бот выведет все профили (адрес admin'а хранится в settings/config.py).
        
## Голосовой помощник
1. **Распознавание речи:**
   - Голосовой помощник способен распознавать команды, произнесенные пользователем.

2. **Выполнение заводских команд:**
   - Голосовой помощник может выполнять изначальные команды и фразы:

     2.1 Команда "Время": ИИ называет время по +3UTC

     2.2 Команда "Выход": ИИ завершает распознавание речи
     
     2.3 Команда "Открой калькулятор": ИИ открывает Windows калькулятор
     
     2.4 Команда "Random": ИИ называет рандомное число от 0 до 10
     
     2.5 Команда "Открой настройки": ИИ открывает панель управления Windows

     2.6 Команда "Открой браузер": ИИ открывает в браузер Яндекс-поисковик
     
3. **Выполнение пользовательских команд:**
   - Голосовой помощник может выполнять команды, добавленные пользователем через телеграм-бота.
     *(команды хранятся в 'users.json' у каждого пользователя)*

# Установка и запуск
1. Установка зависимостей
   - Установите нужные библиотеки и фреймворки, указанные ниже.

2. Запуск телеграм-бота:
   - Запустите файл bot-aiogram.py, зарегистрируйте аккаунт и добавьте команды (по надобности) для голосового помощника.
   
3. Запуск голосового помощника:
   - Запустите файл AIspeaker.py для работы с голосовым помощником. Укажите данные, отправленные боту.

# Дополненительно
В основной директории существует несколько директорий:

1. DB - база данных
   
2. settings - хранение config.py для настроек телеграм-бота
   

Также в основной директории хранятся главные рабочие файлы:

3. AIspeaker.py - голосовой помощник
   
4. bot_aio.py - телеграм бот на aiogram
   
5. README.md
   
6. users.json - файл, созданный для базы данных


# Для работы следует скачать библиотеки:
```
pip install speechrecognition
pip install pyaudio
pip install webbrowser
pip install aiogram
```
