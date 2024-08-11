from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd

# Configuración del navegador
opts = Options()
opts.add_argument("--start-maximized")
opts.add_argument("--disable-extensions")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=ChromeService(), options=opts)

# Navegar a la página
driver.get("https://www.theglobaleconomy.com/")
sleep(1)

# Esperar a que el elemento "Rankings" sea clickeable y hacer clic
wait = WebDriverWait(driver, 10)
rankings_element = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="menu"]/li[6]/a/span'))
)
rankings_element.click()
sleep(1)

# Esperar a que el dropdown esté presente y seleccionable
dropdown_element = wait.until(
    EC.presence_of_element_located((By.XPATH, '//select[@id="regions"]'))
)
dropdown = Select(dropdown_element)
dropdown.select_by_visible_text("Latin America")
sleep(1)

# Esperar a que la tabla esté presente antes de extraer los encabezados
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="benchmarkTable"]')))
sleep(1)

# Extraer los encabezados de la tabla
headers = driver.find_elements(By.XPATH, '//*[@id="benchmarkTable"]/thead/tr/th')
sleep(1)
headers = [header.text for header in headers]

# Extraer datos de la tabla
rows = driver.find_elements(By.XPATH, '//*[@id="benchmarkTable"]/tbody/tr')
sleep(1)

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols]
    data.append(cols)

# Crear DataFrame
df = pd.DataFrame(data, columns=headers)

# Guardar en Excel
# df.to_excel("docs/theglobaleconomy/theglobaleconomy.xlsx", index=False)
df.to_excel("theglobaleconomy.xlsx", index=False)

driver.quit()
