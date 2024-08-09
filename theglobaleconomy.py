from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import pandas as pd
from time import sleep

# Configuración del navegador
opts = Options()

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

opts.add_argument(f"{user_agent=}")
opts.add_argument("--start-maximized")
opts.add_argument("--disable-extensions")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=ChromeService(), options=opts)

# Navegar a la página
driver.get("https://www.theglobaleconomy.com/")
sleep(5)

# Seleccionar "Rankings"
element = driver.find_element(By.XPATH, '//*[@id="menu"]/li[6]/a/span')
element.click()
sleep(3)

# Seleccionar "Latin America" en el dropdown
element = driver.find_element(By.XPATH, '//select[@id="regions"]')
dropdown = Select(element)
dropdown.select_by_visible_text("Latin America")
sleep(3)

# Extraer los encabezados de la tabla
headers = driver.find_elements(By.XPATH, '//*[@id="benchmarkTable"]/thead/tr/th')
headers = [header.text for header in headers]

# Extraer datos de la tabla
rows = driver.find_elements(By.XPATH, '//*[@id="benchmarkTable"]/tbody/tr')

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols]
    data.append(cols)

# Crear DataFrame
df = pd.DataFrame(data, columns=headers)

# Guardar en Excel
df.to_excel("docs/theglobaleconomy/theglobaleconomy.xlsx", index=False)

driver.quit()
