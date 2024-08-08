from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
opts.add_argument("--disable-javascript")

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
# splits_xpath = [
#     '//*[@id="main-container"]/main/section[1]/div[1]/div/button[1]',
#     '//*[@id="main-container"]/main/section[1]/div[1]/div/button[2]',
#     '//*[@id="main-container"]/main/section[1]/div[1]/div/button[5]',
# ]

# for i, split_xpath in enumerate(splits_xpath):
#     element = driver.find_element(By.XPATH, split_xpath)
#     element.click()
#     sleep(1)

#     elements = driver.find_elements(By.XPATH, '//*[@id="standingDesktop"]/div/div')
#     sleep(1)

#     headers = []
#     data = []

#     header_div = elements[0]
#     header_texts = header_div.text.split("\n")
#     headers = header_texts

#     for element in elements[1:]:
#         text_list = element.text.split("\n")
#         data.append(text_list)

#     df = pd.DataFrame(data, columns=headers)
#     df.to_excel(f"kingsleague_spain_split_{i+1}.xlsx", index=False)
#     sleep(1)

# sleep(2)

# Get data for cups spain
# cups_xpath = [
#     '//*[@id="main-container"]/main/section[1]/div[1]/div/button[3]',
#     '//*[@id="main-container"]/main/section[1]/div[1]/div/button[4]',
# ]

# global_index = 1

# for cup_xpath in cups_xpath:
#     element = driver.find_element(By.XPATH, cup_xpath)
#     element.click()
#     sleep(1)
#     elements = driver.find_elements(
#         By.XPATH, '//*[@id="main-container"]/main/section[1]/div[2]/div'
#     )
#     sleep(1)
#     for sub_element in elements:
#         group_element = sub_element.find_element(By.XPATH, ".//div")
#         sleep(1)

#         group_split = group_element.text.split("\n")
#         group = "_".join(group_split)

#         table_elements = sub_element.find_elements(
#             By.XPATH, './/div[@id="standingDesktop"]/div/div'
#         )
#         sleep(1)

#         headers = []
#         data = []

#         header_div = table_elements[0]
#         header_texts = header_div.text.split("\n")
#         headers = header_texts

#         for element in table_elements[1:]:
#             text_list = element.text.split("\n")
#             data.append(text_list)

#         df = pd.DataFrame(data, columns=headers)
#         df.to_excel(
#             f"kingsleague_spain_cup_{group}_table_{global_index}.xlsx", index=False
#         )
#         global_index += 1

# Americas
element = driver.find_element(By.XPATH, '//*[@id="navbar-regions"]/ul/li[2]/a')
element.click()
sleep(1)

element = driver.find_element(By.XPATH, '//*[@id="competitionNavbar"]')
element.click()
sleep(1)

element = driver.find_element(
    By.XPATH, '//*[@id="dropdownCompetitionNavbar"]/ul/li[2]/a'
)
element.click()
sleep(4)

element = driver.find_element(
    By.XPATH, '//*[@id="main-container"]/main/section[1]/div[1]/div/button'
)
element.click()
sleep(1)

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
df.to_excel(f"kingsleague_americas_split_1.xlsx", index=False)

sleep(2)

driver.quit()
