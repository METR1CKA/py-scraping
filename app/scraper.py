# app/scraper.py


from app.utils.base_scraper import BaseScraper
from config.instructions import Instructions
from app.classes.scripts import Scripts


class Scraper(BaseScraper):
    def __init__(self, instructions: Instructions, config, file):
        self.scripts = Scripts(self)
        self.super = super()
        self.instructions = instructions
        self.config = config.strip()
        self.json = file
        self.specifiedActions = {
            "MODAL": self.scripts.modal,
            "EXTRACT-PLACES": self.scripts.extractPlaces,
            "SPAIN-SPLITS": self.scripts.splits,
            "SPAIN-CUPS": self.scripts.cups,
            "AMERICAS-SPLITS": self.scripts.splits,
            "EXTRACT-DIVS": self.scripts.extractTableDivs,
            "EXTRACT-TABLE": self.scripts.extractTable,
            "EXTRACT-TABLES": self.scripts.extractTables,
            "HOF-TABLE": self.scripts.hallOfFameTable,
            "METEORED": {},
        }

    def run(self):
        # Obtener los pasos a seguir
        steps = self.instructions.getElement(self.config, "steps")
        if steps is None:
            print("\nNo se encontraron pasos para este archivo.")
            return
        # Inicializar la clase BaseScraper
        self.super.__init__()
        # Iterar sobre los pasos
        for step in steps:
            # Obtener los datos del paso
            action, data = (
                step.get("action"),
                step.get("data"),
            )
            # Setear los datos del paso
            self.setData(data)
            # Verificar si la acción es válida para las acciones comunes
            action = action.upper().strip()
            if action in self.commonActions.keys():
                self.commonActions[action]()
            # Verificar si la acción es válida para las acciones especificadas
            if action in self.specifiedActions.keys():
                self.specifiedActions[action]()
        # Salir del navegador
        self.waitTime(1)
        self.quit()
