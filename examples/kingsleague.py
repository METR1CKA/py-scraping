# example/kingsleague.py
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
driver.get("https://kingsleague.pro/es/espana")
sleep(5)

# Desactivar cookies
element = driver.find_element(By.XPATH, '//*[@id="lw-banner"]/div/div[2]/div/button[2]')
element.click()
sleep(1)

# Competiciones
element = driver.find_element(By.XPATH, '//button[@id="competitionNavbar"]')
element.click()
sleep(1)

# Calificaciones
element = driver.find_element(
    By.XPATH, '//*[@id="dropdownCompetitionNavbar"]/ul/li[2]/a'
)
element.click()
sleep(4)

# Get data for splits spain
splits_indexes = [
    1,
    2,
    5,
]

for i, split_index in enumerate(splits_indexes):
    element = driver.find_element(
        By.XPATH,
        f'//*[@id="main-container"]/main/section[1]/div[1]/div/button[{split_index}]',
    )
    element.click()
    sleep(5)

    elements = driver.find_elements(By.XPATH, '//*[@id="standingDesktop"]/div/div')
    sleep(1)

    headers = []
    data = []

    header_div = elements[0]
    header_texts = header_div.text.split("\n")
    headers = header_texts

    for element in elements[1:]:
        text_list = element.text.split("\n")
        data.append(text_list)

    df = pd.DataFrame(data, columns=headers)
    df.to_excel(f"docs/kingsleague/spain/splits/split_{i+1}.xlsx", index=False)
    sleep(1)

# Get data for cups spain
cups_indexes = [
    3,
    4,
]

for cup_index in cups_indexes:
    element = driver.find_element(
        By.XPATH,
        f'//*[@id="main-container"]/main/section[1]/div[1]/div/button[{cup_index}]',
    )
    element.click()
    sleep(5)
    elements = driver.find_elements(
        By.XPATH, '//*[@id="main-container"]/main/section[1]/div[2]/div'
    )
    sleep(1)

    fullname = f"docs/kingsleague/spain"
    if cup_index == 3:
        fullname = f"{fullname}/kings_cup"
    if cup_index == 4:
        fullname = f"{fullname}/kingdom_cup"

    for sub_element in elements:
        group_element = sub_element.find_element(By.XPATH, ".//div")
        sleep(1)

        group_split = group_element.text.split("\n")
        group = "_".join(group_split)

        table_elements = sub_element.find_elements(
            By.XPATH, './/div[@id="standingDesktop"]/div/div'
        )
        sleep(1)

        headers = []
        data = []

        header_div = table_elements[0]
        header_texts = header_div.text.split("\n")
        headers = header_texts

        for element in table_elements[1:]:
            text_list = element.text.split("\n")
            data.append(text_list)

        df = pd.DataFrame(data, columns=headers)
        df.to_excel(
            f"{fullname}/{group}.xlsx",
            index=False,
        )

# Americas
element = driver.find_element(By.XPATH, '//*[@id="navbar-regions"]/ul/li[2]/a')
element.click()
sleep(2)

element = driver.find_element(By.XPATH, '//*[@id="competitionNavbar"]')
element.click()
sleep(2)

element = driver.find_element(
    By.XPATH, '//*[@id="dropdownCompetitionNavbar"]/ul/li[2]/a'
)
element.click()
sleep(4)

element = driver.find_element(
    By.XPATH, '//*[@id="main-container"]/main/section[1]/div[1]/div/button'
)
element.click()
sleep(5)

elements = driver.find_elements(By.XPATH, '//*[@id="standingDesktop"]/div/div')
sleep(1)

headers = []
data = []

header_div = elements[0]
header_texts = header_div.text.split("\n")
headers = header_texts

for element in elements[1:]:
    text_list = element.text.split("\n")
    data.append(text_list)

df = pd.DataFrame(data, columns=headers)
df.to_excel("docs/kingsleague/americas/split_1.xlsx", index=False)

sleep(2)

driver.quit()
