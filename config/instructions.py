# config/instructions.py


from config.app import App
import json


class Instructions:
    def __init__(self, folders=["instructions", "json"]):
        app = App()
        self.data = {}
        jsonDir = app.joinPath(*folders)
        jsonFiles = app.listDir(jsonDir)
        for filename in jsonFiles:
            if filename.endswith(".json"):
                filepath = app.joinPath(jsonDir, filename)
                with open(filepath, "r") as file:
                    configName = filename.split(".")[0]
                    self.data[configName] = json.load(file)

    def get(self, config, key, default=None):
        return self.data[config].get(key, default) if self.data else default
