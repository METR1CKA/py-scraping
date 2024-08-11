# main.py


from cli.menu import Menu
import sys


def main():
    menu = Menu()
    menu.display("Menú principal")

    while True:
        choice = menu.get()
        if "Salir" in choice:
            print("\nSaliendo del programa...\n")
            break
        print(f"\nSeleccionaste: {choice}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaliendo...\n")
        sys.exit(0)
