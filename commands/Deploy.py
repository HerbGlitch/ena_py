import sys
import datetime
import os
import os.path
import getpass
import subprocess as s
import platform


class Deploy(object):

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_user = getpass.getuser()

    def main(self):
        for i in range(30):
            print()
        print("Beginning automated deployment using python.")
        git_installed = input("Is git installed? y/N ")
        heroku_installed = input("Is the heroku cli installed? y/N ")
        print("Current Directory is: " + self.current_dir)
        print("Current User is: " + self.current_user)
        if git_installed.lower() == "y" and heroku_installed.lower() == "y":
            self.write_siteinfo()
            self.write_gitignore()
            self.deploy()
        else:
            print("Please install git and heroku before proceeding.")

    def write_siteinfo(self):
        commit_message = input("Please enter a commit message: ")
        print("Checking if siteinfo.html exists in homepage/templates/")
        if os.path.isfile(self.current_dir + "/homepage/templates/siteinfo.html"):
            print("Siteinfo exists.  Writing datetime and user now.")
            siteinfo = open(self.current_dir + "/homepage/templates/siteinfo.html", 'w+')
            siteinfo.write("The current release is: " + self.current_datetime)
            siteinfo.write("<br>")
            siteinfo.write(self.current_user + " commit message: " + commit_message)
            siteinfo.close()
        else:
            print("Siteinfo does not exist.  Creating now...")
            siteinfo = open(self.current_dir + "/homepage/templates/siteinfo.html", 'w+')
            siteinfo.write("The current release is: " + self.current_datetime)
            siteinfo.write("<br>")
            siteinfo.write(self.current_user + " commit message: " + commit_message)
            siteinfo.close()

    def write_gitignore(self):
        print("Creating and rewriting .gitignore")
        try:
            gitignore = open(".gitignore", "w+")
            gitignore.write(".elasticbeanstalk/*\n")
            gitignore.write("!.elasticbeanstalk/*.cfg.yml\n")
            gitignore.write("!.elasticbeanstalk/*.global.yml\n")
            gitignore.write("\n")
            gitignore.write("homepage/.cached_templates\n")
            gitignore.write("hompage/templates/.cached_templates\n")
            gitignore.write(".DS_Store\n")
            gitignore.write("/.DS_Store\n")
            gitignore.write("/.Python\n")
            gitignore.write("/bin/\n")
            gitignore.write("/include/\n")
            gitignore.write("/lib/\n")
            gitignore.write("/pip-selfcheck.json\n")
            gitignore.close()
        except:
            print(".gitignore failed to open or create.")


    def write_pip_freeze(self):
        print("Please make sure your virtual environment is activated.  Detection is disabled in this version of ENA.")
        if platform.system() == "Windows":
            print("Windows system detected.")
            print("Pip freezing")
            s.run(["pip", "freeze", ">", "requirements.txt"])
        elif platform.system() == "Linux":
            print("Linux machine detected.")
            print("Pip freezing and removing pkg-resources")
            s.run(["pip3", "freeze", ">", "requirements.txt"])
            s.run(["sed", "-i", "'/pkg-resources/d'", "./requirements.txt"])
        elif platform.system() == "Mac":
            print("Mac detected.")
            print("Macs are not supported at this time.  Please upgrade your version of ena with the upgrade command.")


    def deploy(self):
        print("Beginning deploy...")
        s.run(["git", "add", "."])
        s.run(["git", "commit", "-am", "\"Automated deployment commit\""])
        s.run(["git", "push", "heroku", "master", "-f"])
