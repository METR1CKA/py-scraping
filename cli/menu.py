# cli/menu.py


from config.instructions import Instructions


class Menu:
    def __init__(self):
        self.json = Instructions()
        self.options = {
            key: value.split(".")[0]
            for key, value in enumerate(self.json.showJsons(), 1)
        }
        self.options[len(self.options) + 1] = "Salir"

    def display(self, title):
        print(f"------ {title} ------")
        for key, value in self.options.items():
            print(f"{key}. {value}")

    def get(self):
        choice = None
        while choice is None:
            try:
                choice = int(input("\nSelecciona una opción: "))
                if not choice in self.options:
                    print("\nOpción inválida")
                    choice = None
            except ValueError:
                print("\nPor favor, seleccione un número válido.")
                choice = None
        return self.options[choice]

    def executeChoice(self, option):
        try:
            pass
        except Exception as e:
            pass
