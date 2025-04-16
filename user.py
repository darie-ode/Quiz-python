# user.py
import json
import os

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                return json.load(file)
        return {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def get_user(self, username):
        return self.users.get(username)

    def update_user(self, username, data):
        self.users[username] = data
        self.save_users()

    def get_all_users(self):
        return self.users
