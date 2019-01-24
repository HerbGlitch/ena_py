from passlib.hash import pbkdf2_sha256
import psycopg2
import getpass
import easygui

class User:
    #Objects
    id = None
    username = None
    password = None
    level = None
    #Booleans
    logged_in = False
    #Arrays
    #this arry will hold .bat files for work projects
    projects = []

    #constructor
    def user(self, id, username, password, level):
        self.id = id
        self.username = username
        self.password = password
        self.level = level


    #checks for a level key then if it is correct, the level changes
    def change_level(self, level_key, level_num):
        if(pbkdf2_sha256.encrypt(level_key, rounds=200000, salt_size=16)):
            self.level = level_num
            print("level changed")
        else:
            print("key incorrect")

    #changes username
    def change_username(self, new_username):
        self.username = new_username
        print("username changed")

    #creates password
    def create_password(self, password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    #checks password against hashed password, if they are equal, the password changes
    def change_password(self, new_password):
        if(pbkdf2_sha256.encrypt(new_password, rounds=200000, salt_size=16)):
            self.password = new_password
            print("Password changed")
        else:
            print("Password incorrect")

    #creates a .bat file that goes to work project location then activates the virtual enviroment and runs the server
    def create_run_file(self):
        name = input("name of bat file: ")
        file = open(name + ".bat", "w+")
        location = input("file to run name: ")
        file.write("cd C:\\Users\\HerbGlitch\\BrightBridgeWeb\\Desktop\\" + location + "\\" + location + "env\n")
        file.write("call scripts\\activate\n")
        file.write("cd ..\n")
        file.write("cd " + location + "\n")
        file.write("call atom .\n")
        file.write("call cls\n")
        file.write("call python manage.py runserver")
        file.close()
        self.projects.append(file)

    def show_info(self):
        print("Level: " + str(self.level))
        print("username: " + str(self.username))

    def user_login(self, password, test_password):
        test = pbkdf2_sha256.verify(password, self.password)
        return test
