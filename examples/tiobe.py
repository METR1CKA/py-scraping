from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
wait = WebDriverWait(driver, 10)

# Navegar a la página
driver.get("https://www.tiobe.com/")
sleep(1)

# Esperar y denegar cookies
cookie_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="CybotCookiebotDialogBodyButtonDecline"]')
    )
)
cookie_button.click()
sleep(1)

# Ir a las tablas de popularidad
menu_item = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//li[@id="menu-item-1184"]/a'))
)
menu_item.click()
sleep(1)

# Extraer encabezados del top 20
element = wait.until(
    EC.presence_of_element_located((By.XPATH, "/html/body/section/div/article/p[2]"))
)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

element = wait.until(
    EC.presence_of_element_located((By.XPATH, "/html/body/section/div/article/p[3]"))
)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

headers = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="top20"]/thead/tr/th'))
)
sleep(1)
headers = [header.text for header in headers]

# Ajustar encabezados eliminando "Change" si es necesario
first_change_index = headers.index("Change") if "Change" in headers else -1
if first_change_index != -1:
    headers = [
        header
        for i, header in enumerate(headers)
        if header != "Change" or i > first_change_index
    ]

# Extraer datos de la tabla
rows = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="top20"]/tbody/tr'))
)
sleep(1)
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols if col.text.strip() != ""]
    data.append(cols)

# Crear DataFrame y guardar en Excel
df = pd.DataFrame(data, columns=headers)
# df.to_excel("docs/tiobe/Top20.xlsx", index=False)
df.to_excel("Top20.xlsx", index=False)

# Extraer Otros lenguajes de programación
container = wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="container"]'))
)
driver.execute_script("arguments[0].scrollIntoView();", container)
sleep(1)

element = wait.until(
    EC.presence_of_element_located((By.XPATH, "/html/body/section/div/article/h2[1]"))
)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

headers = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="otherPL"]/thead/tr/th'))
)
sleep(1)
headers = [header.text for header in headers]

rows = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="otherPL"]/tbody/tr'))
)
sleep(1)
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=headers)
# df.to_excel("docs/tiobe/OtherProgrammingLanguages.xlsx", index=False)
df.to_excel("OtherProgrammingLanguages.xlsx", index=False)

# Extraer Lenguajes de programación con más Historia de muy largo plazo
element = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "/html/body/section/div/article/ul[1]/li")
    )
)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

headers = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="VLTH"]/thead/tr/th'))
)
sleep(1)
headers = [header.text for header in headers]

rows = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="VLTH"]/tbody/tr'))
)
sleep(1)
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=headers)
# df.to_excel("docs/tiobe/VeryLongTermHistory.xlsx", index=False)
df.to_excel("VeryLongTermHistory.xlsx", index=False)

# Extraer Lenguajes de programación del salón de la fama
element = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "/html/body/section/div/article/ul[2]/li[2]")
    )
)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

element = wait.until(
    EC.presence_of_element_located((By.XPATH, "/html/body/section/div/article/p[10]"))
)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

rows = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="PLHoF"]/tbody/tr'))
)
sleep(1)
headers = []
data = []
for i, row in enumerate(rows):
    if i == 0:
        headers = row.find_elements(By.TAG_NAME, "th")
        headers = [header.text for header in headers]
    else:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols = [col.text for col in cols]
        data.append(cols)

df = pd.DataFrame(data, columns=headers)
# df.to_excel("docs/tiobe/ProgrammingLanguageHallOfFame.xlsx", index=False)
df.to_excel("ProgrammingLanguageHallOfFame.xlsx", index=False)

driver.quit()
