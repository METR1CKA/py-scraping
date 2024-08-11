# cli/menu.py


from config.instructions import Instructions
from app.scraper import Scraper


class Menu:
    def __init__(self):
        self.instructions = Instructions()
        self.jsons = self.instructions.showJsons()
        self.options = {
            key: value.split(".")[0] for key, value in enumerate(self.jsons, 1)
        }
        self.options[len(self.options) + 1] = "Salir"

    def display(self, title):
        print(f"------ {title} ------")
        for key, value in self.options.items():
            print(f"{key}. {value}")

    def get(self):
        option_number = None
        while option_number is None:
            try:
                option_number = int(input("\nSelecciona una opción: "))
                if not option_number in self.options:
                    print("\nOpción inválida")
                    option_number = None
            except ValueError:
                print("\nPor favor, seleccione un número válido.")
                option_number = None
        option_name = self.options[option_number]
        return option_name, option_number

    def executeChoice(self, optionName, optionNumber):
        file = self.jsons[optionNumber - 1]
        scraper = Scraper(self.instructions, optionName, file)
        scraper.run()
