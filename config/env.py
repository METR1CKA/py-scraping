# config/env.py


from config.app import App
import dotenv


class Env:
    def __init__(self, file=".env"):
        app = App()
        self.envPath = app.joinPaths(file)
        dotenv.load_dotenv(self.envPath)
        if not app.exists(self.envPath):
            raise FileNotFoundError(f"No se encontró el archivo {file}")

    def setEnv(self, key, value):
        dotenv.set_key(self.envPath, key, value)

    def getEnv(self, key):
        return dotenv.get_key(self.envPath, key)
