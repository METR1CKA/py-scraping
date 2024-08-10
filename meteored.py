from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from time import sleep

# Configuración del navegador
opts = Options()
opts.add_argument("--start-maximized")
opts.add_argument("--disable-extensions")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=ChromeService(), options=opts)

driver.get("https://www.meteored.mx/")
sleep(5)

cities = ["Torreón", "Gomez Palacio", "Monterrey"]

for city in cities:
    # Acumular datos
    full_data = []

    # Ingresar la primer ciudad
    element = driver.find_element(By.XPATH, '//*[@id="search_pc"]')
    element.send_keys(city)
    sleep(3)

    # Seleccionar la primera opción
    element = driver.find_element(By.XPATH, '//*[@id="resultados"]/ul/li[1]')
    element.click()
    sleep(3)

    # Seleccionar los dias
    days_indexes = [
        4,
        5,
    ]

    for day_index in days_indexes:
        # Ir a la sección de los días
        element = driver.find_element(
            By.XPATH,
            f"/html/body/main/div[2]/section/section[2]/div/ul/li[{day_index}]/span",
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(3)
        element.click()
        sleep(3)

        # Obtener los datos
        elements = driver.find_elements(
            By.XPATH, "/html/body/div[1]/div[1]/section/div/table/tbody[2]/tr"
        )
        data = [element.text for element in elements]
        data = [entry for entry in data if entry]

        # Procesar los datos
        process_data = []
        for entry in data:
            parts = entry.split("\n")
            hora, temperatura, sensacion_termica, viento, velocidad, indice_uv, fps = (
                parts
            )
            process_data.append(
                {
                    "Hora": hora,
                    "Temperatura": temperatura,
                    "Sensación Termica": sensacion_termica,
                    "Viento": viento,
                    "Velocidad": velocidad,
                    "Índice UV": indice_uv,
                    "FPS": fps,
                }
            )
        full_data += process_data

    # Crear DataFrame y guardar en archivo Excel
    df = pd.DataFrame(full_data)
    df.to_excel(f"docs/meteored/{city}.xlsx", index=False)

    # Regresar a la página principal
    driver.execute_script("window.scrollTo(0, 0);")
    sleep(3)

driver.quit()
