# app/scraper.py


from app.classes.kingsleague import KingsLeague
from app.utils.pandas_df import PandasDataFrame
from app.utils.base_scraper import BaseScraper
from config.instructions import Instructions
from app.classes.airbnb import Airbnb


class Scraper(BaseScraper):
    def __init__(self, instructions: Instructions, config, file):
        self.airbnb = Airbnb(self)
        self.kingsleague = KingsLeague(self)
        self.super = super()
        self.instructions = instructions
        self.config = config.strip()
        self.json = file
        self.specifiedActions = {
            "AIRBNB": {
                "MODAL": self.airbnb.modal,
                "PROCESS-ELEMENTS": self.airbnb.processElements,
            },
            "KINGSLEAGUE": {
                "SPAIN-SPLITS": self.kingsleague.splits,
                "SPAIN-CUPS": self.kingsleague.cups,
                "AMERICAS-SPLITS": self.kingsleague.splits,
            },
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
            config = self.config.upper()
            if config in self.specifiedActions.keys():
                specifiedActions = self.specifiedActions[config]
                if action in specifiedActions.keys():
                    specifiedActions[action]()
        # Salir del navegador
        self.waitTime(1)
        self.quit()
