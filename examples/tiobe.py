# examples/tiobe.py
from selenium.webdriver.chrome.service import Service as ChromeService
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

# Navegar a la página
driver.get("https://www.tiobe.com/")
sleep(5)

# Denegar cookies
element = driver.find_element(
    By.XPATH, '//*[@id="CybotCookiebotDialogBodyButtonDecline"]'
)
element.click()
sleep(1)

# Ir a las tablas de popularidad
element = driver.find_element(By.XPATH, '//li[@id="menu-item-1184"]/a')
element.click()
sleep(2)

# Extraer encabezados del top 20
element = driver.find_element(By.XPATH, "/html/body/section/div/article/p[2]")
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

element = driver.find_element(By.XPATH, "/html/body/section/div/article/p[3]")
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

headers = driver.find_elements(By.XPATH, '//*[@id="top20"]/thead/tr/th')
headers = [header.text for header in headers]
sleep(1)

first_change_index = headers.index("Change") if "Change" in headers else -1
if first_change_index != -1:
    headers = [
        header
        for i, header in enumerate(headers)
        if header != "Change" or i > first_change_index
    ]

rows = driver.find_elements(By.XPATH, '//*[@id="top20"]/tbody/tr')
sleep(1)

data = []

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols if col.text.strip() != ""]
    data.append(cols)

df = pd.DataFrame(data, columns=headers)
df.to_excel("docs/tiobe/Top20.xlsx", index=False)
sleep(1)

# Extraer Otros lenguajes de programación
element = driver.find_element(By.XPATH, '//*[@id="container"]')
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

element = driver.find_element(By.XPATH, "/html/body/section/div/article/h2[1]")
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

headers = driver.find_elements(By.XPATH, '//*[@id="otherPL"]/thead/tr/th')
headers = [header.text for header in headers]
sleep(1)

rows = driver.find_elements(By.XPATH, '//*[@id="otherPL"]/tbody/tr')
sleep(1)

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=headers)
df.to_excel("docs/tiobe/OtherProgrammingLanguages.xlsx", index=False)
sleep(1)

# Extraer Lenguajes de programación con mas Historia de muy largo plazo
element = driver.find_element(By.XPATH, "/html/body/section/div/article/ul[1]/li")
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

headers = driver.find_elements(By.XPATH, '//*[@id="VLTH"]/thead/tr/th')
headers = [header.text for header in headers]
sleep(1)

rows = driver.find_elements(By.XPATH, '//*[@id="VLTH"]/tbody/tr')
sleep(1)

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=headers)
df.to_excel("docs/tiobe/VeryLongTermHistory.xlsx", index=False)

# Extraer Lenguajes de programación del salón de la fama
element = driver.find_element(By.XPATH, "/html/body/section/div/article/ul[2]/li[2]")
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

element = driver.find_element(By.XPATH, "/html/body/section/div/article/p[10]")
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(1)

rows = driver.find_elements(By.XPATH, '//*[@id="PLHoF"]/tbody/tr')
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
df.to_excel("docs/tiobe/ProgrammingLanguageHallOfFame.xlsx", index=False)
sleep(1)

driver.quit()
