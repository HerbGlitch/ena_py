import sys
import os


class Commands():
	#objects
	#vars set to null
	ena = None
	deploy = None
	scheduler = None
	#integers
	highest_user_number = None
    #arrays
	commands_array = {}

	# constructor
	def commands(self, ena, deploy, scheduler):
		# created to make it possible to call user or ena without making a new instance
		self.ena = ena
		self.deploy = deploy
		self.scheduler = scheduler
		self.load_commands_abstract_user()

	def load_commands_abstract_user(self):
		temp_array = {
			#command functions cannot have parameters
			#'command name': call.command.with.no.parameters,
			#top of help
			'help': self.ena.ena_help,
			#no level
			'login': self.ena.login,
			'create user': self.ena.edit_users.create_user,
			#bottom of help
			'exit': self.exit,
		}
		self.commands_array = temp_array

	def load_commands_authenticated_user(self):
		self.highest_user_number = self.ena.main_user.level
		temp_array = {
			#command functions cannot have parameters
			#'command name': [call.command.with.no.parameters, level number],
			#top of help
			'help': [self.ena.ena_help, self.highest_user_number],
			'show profile information': [self.ena.main_user.show_info, self.highest_user_number],
			#level 1
			'deploy': [self.deploy.main, 1],
			'schedule': [self.scheduler.main, 1],
			#admin
			'change user level': [self.ena.change_user_level, 0],
			'create run file': [self.ena.main_user.create_run_file, 0],
			'show all users information': [self.ena.show_users, 0],
			#bottom of help
			'logout': [self.ena.logout, self.highest_user_number],
			'exit': [self.exit, self.highest_user_number],
		}
		level_temp_array = self.load_level_commands(temp_array)
		self.commands_array = level_temp_array

	def load_level_commands(self, array):
		temp_dictionary = {}
		for key in array:
			if(array[key][1] >= self.ena.main_user.level):
				temp_dictionary[key] = array[key]
		return temp_dictionary

	def test_commands(self, command):
		# if(self.user == None and levels_loaded)
		command = command.lower()
		self.ena.clear()
		real_command = False
		for key in self.commands_array:
			if(key == command):
				self.label(command)
				if(self.ena.main_user == None):
					self.commands_array[key]()
				else:
					self.commands_array[key][0]()
				real_command = True
		if(not real_command):
			print("I am sorry, I did not get that.")

	def label(self, label):
		#labels look like ----LABEL----
		print("----" + label.upper() + "----")

	def exit(self):
		#clears screen then exits program
		self.ena.clear()
		exit()
