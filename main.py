# main.py


from config.app import App
from cli.menu import Menu


def main(app: App):
    menu = Menu()
    app.clear()
    menu.display("Menú principal")
    while True:
        option_name, option_number = menu.get()
        if "Salir" in option_name:
            print("\nSaliendo del programa...\n")
            break
        menu.executeChoice(optionName=option_name, optionNumber=option_number)
        # try:
        # except Exception as e:
        #     print(f"Error: {e}")
        #     app.exit(1)


if __name__ == "__main__":
    application = App()
    try:
        main(app=application)
    except KeyboardInterrupt:
        print("\n\nSaliendo...\n")
        application.exit(0)
