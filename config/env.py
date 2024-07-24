# config/env.py


from dotenv import load_dotenv, get_key, set_key
from config.app import App


class Env:
    def __init__(self, file=".env"):
        app = App()
        self.envPath = app.joinPath(file)
        load_dotenv(self.envPath)
        if not app.exists(self.envPath):
            raise FileNotFoundError(f"No se encontró el archivo {file}")

    def setEnv(self, key, value):
        set_key(self.envPath, key, value)

    def getEnv(self, key):
        return get_key(self.envPath, key)
