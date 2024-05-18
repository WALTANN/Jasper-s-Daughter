import json
import os

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.users = json.load(file)
        else:
            self.users = {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, user_id, name, login, password):
        if str(user_id) in self.users:
            raise ValueError("Пользователь с таким ID уже существует.")
        if any(user['login'] == login for user in self.users.values()):
            raise ValueError("Пользователь с таким логином уже существует.")
        self.users[str(user_id)] = {
            'name': name,
            'login': login,
            'password': password,
            'commands': []
        }
        self.save_data()
        
    def get_user(self, user_id):
        return self.users.get(str(user_id))

    def update_password(self, user_id, new_password):
        user = self.get_user(user_id)
        if user:
            user['password'] = new_password
            self.save_data()
        else:
            raise ValueError("Пользователь не найден.")

    def update_username(self, user_id, new_username):
        user = self.get_user(user_id)
        if user:
            user['name'] = new_username
            self.save_data()
        else:
            raise ValueError("Пользователь не найден.")
