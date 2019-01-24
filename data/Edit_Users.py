from passlib.hash import pbkdf2_sha256
from user.User import User
import psycopg2
import getpass
import easygui

class Edit_Users():
    ena = None

    def Edit_Users(self, ena):
        self.ena = ena

    def load_users(self):
        conn = psycopg2.connect(self.ena.conn_string)
        cursor = conn.cursor()
        id = 0
        level = 0
        cursor.execute("SELECT * FROM Users;")
        # Remember to add fields added to the user constructor here.
        # To add the fields to the column add them in settings.py
        for user_info in cursor:
            user = User()
            user.user(user_info[0], user_info[1], user_info[2], user_info[3])
            self.ena.users.append(user)
            id = user_info[0]
        conn.commit()
        conn.close()
        return id

    def create_user(self):
        user = User()
        conn = psycopg2.connect(self.ena.conn_string)
        cursor = conn.cursor()
        username = input("username: ")
        password = getpass.getpass("Password: ")
        testing_password = getpass.getpass("Confirm Password: ")
        if(password == testing_password):
            password = user.create_password(password)
            level = 1
            self.ena.id += 1
            cursor.execute("INSERT INTO Users VALUES(%s,%s,%s,%s)", (self.ena.id, username, password, level))
            conn.commit()
            conn.close()
            user.user(id, username, password, level)
            self.ena.users.append(user)
            self.ena.users[self.ena.id-1].logged_in = True
            self.ena.main_user = user
            self.ena.commands.load_commands_authenticated_user()
        else:
            conn.commit()
            conn.close()
            print("passwords did not match")
