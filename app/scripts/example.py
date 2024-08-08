# from config.env import Env
import dotenv


class Example:
    def __init__(self):
        # self.env = Env()
        pass

    def get(self):
        # return self.env.getEnv("USER_AGENT")
        return dotenv.get_key("../../.env", "USER_AGENT")


if __name__ == "__main__":
    example = Example()
    print(example.get())
