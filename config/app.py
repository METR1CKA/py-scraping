# config/app.py


import os, sys


class App:
    def __init__(self):
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def getRoot(self):
        return self.root

    def joinPaths(self, *args):
        return os.path.join(self.root, *args)

    def exists(self, path):
        return os.path.exists(path)

    def makeDirs(self, path):
        os.makedirs(path)

    def listDir(self, path):
        return os.listdir(path)

    def clear(self):
        os.system("clear")

    def exit(self, code):
        sys.exit(code)
