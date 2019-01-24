import os
from os.path import expanduser


class Scheduler(object):
    folderpath = None
    def main(self):
        self.set_folderpath()
        print("Object Created.")
        if not os.path.exists(self.folderpath):
            os.makedirs(self.folderpath + "/.ena")

    def set_folderpath(self):
        self.folderpath = expanduser("~")
