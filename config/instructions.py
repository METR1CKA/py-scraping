# config/instructions.py


from config.app import App
import json


class Instructions:
    def __init__(self):
        self.app = App()
        self.data = {}
        jsonDir = self.dirs()
        jsonFiles = self.showJsons(jsonDir)
        for filename in jsonFiles:
            if filename.endswith(".json"):
                filepath = self.app.joinPaths(jsonDir, filename)
                with open(filepath, "r") as file:
                    configName = filename.split(".")[0]
                    self.data[configName] = json.load(file)

    def dirs(self, folders=["instructions", "json"]):
        return self.app.joinPaths(*folders)

    def showJsons(self, jsonDir=None):
        return self.app.listDir(jsonDir if jsonDir else self.dirs())

    def getElement(self, config, key=None, default=None):
        if key is None:
            return self.data.get(config, default)
        return self.data[config].get(key, default)
