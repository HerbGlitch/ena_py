import os
from data.Edit_Users import Edit_Users
from user.User import User
from commands.Commands import Commands
from commands.Deploy import Deploy
from commands.Scheduler import Scheduler
from data.settings import create_tables
import getpass
from os.path import expanduser


class ENA():
    HOME = expanduser("~")
    # Booleans
    running = False
    # Objects
    edit_users = Edit_Users()
    commands = Commands()
    deploy = Deploy()
    scheduler = Scheduler()

    main_user = None
    ena = None
    # edit_users = None
    # commands = None
    # deploy = None
    # scheduler = None
    id = None
    # Strings
    conn_string = "host='localhost' dbname='enabrain' user='postgres' password='ra'"
    # Array for users
    users = []

    #constructor
    def ena(self, ena):
        self.running = True
        self.ena = ena
        #Creates the commands
        self.edit_users.Edit_Users(ena)
        self.commands.commands(self.ena, self.deploy, self.scheduler)
        try:
            #Checks if there is a table, if so, it loads the users
            self.id = self.edit_users.load_users()
        except:
            #Creates tables then loads empty users and sets the user id to 0
            Create_Tables = create_tables()
            Create_Tables.create_tables(ena)
            self.id = self.edit_users.load_users()
        self.ena.run()

    #this command is used in Commands.py
    def ena_help(self):
        print("=======================================")
        if(self.main_user == None):
            for command in self.commands.commands_array:
                print(command)
        else:
            for command in self.commands.commands_array:
                print(command)
        print("=======================================")

    #Admin function
    def show_users(self):
        for user in self.users:
            print("=======================================")
            user.show_info()
            print("=======================================")

    def change_user_level(self):
        selected_user = input("please enter the user you want to change their level: ")
        real_user = False
        for user in self.users:
            if(user.username == selected_user):
                real_user = True
                check = input("Are you sure you want to change "+selected_user+"'s level: ")
                level = int(input("please enter the user's new level: "))
                if(check.lower() == "yes" or check.lower() == "y"):
                    user.level = level
                    print(user.username+" is now a level " + str(user.level))
                else:
                    print("Authorization cancled")
        if(not real_user):
            print("There is no user with that username.")

    def login(self):
        testing_username = input("username: ")
        authenticate = False
        for user in self.users:
            #check for the username in the database
            if(user.username == testing_username):
                authenticate = True
                #checks password based of the id, the id is minus one because the array starts at zero and the id starts at one
                temp_id = user.id
                testing_password = getpass.getpass("Password: ")
                test = self.users[temp_id-1].user_login(testing_password, user.password)
                #logs in user
                if(test):
                    user.logged_in = True
                    self.main_user = user
        #this checks if the user is logged in, checks if they are admin, then lets them know they are logged in
        if(not self.main_user == None):
            self.commands.load_commands_authenticated_user()
            self.clear()
            if(self.main_user.level == 0):
                print("----ADMIN----")
            print(self.main_user.username + ", You are now logged in")
        #this lets the user know that their password or username is incorrect
        else:
            if(not authenticate):
                false_pass = getpass.getpass("Password: ")
            print("username or password is incorrect")

    def logout(self):
        #this logs them out, as the functions name implies
        for user in self.users:
            user.logged_in = False
        self.main_user = None
        self.commands.load_commands_abstract_user()
        print("You are now logged out")

    def clear(self):
        #check if the user is using windows
        if os.name == 'nt':
            os.system('cls')
        #else it uses linux termianls 'clear'
        else:
            os.system('clear')

    def run(self):
        self.clear()
        #gets commands
        command = input("Hello, my name is Ena, how may I assist you today: ")
        #main running loop
        while(self.running):
            self.commands.test_commands(command)
            command = input("How may I assist you today: ")


def instantiate():
    ena = ENA()
    ena.ena(ena)

if __name__ == '__main__':
    instantiate()
