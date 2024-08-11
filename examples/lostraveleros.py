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
driver.get("https://lostraveleros.com/")
sleep(5)

element = driver.find_element(
    By.XPATH, '//*[@id="tie-block_897"]/div/div/div/form/label/input'
)
element.send_keys("25 curiosidades de méxico")
sleep(1)
element.submit()
sleep(3)

element = driver.find_element(By.XPATH, '//*[@id="posts-container"]/li[1]/div/a')
element.click()
sleep(3)

element = driver.find_element(By.XPATH, '//*[@id="the-post"]/div[1]/p[1]')
sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", element)
sleep(5)

headers = driver.find_elements(By.XPATH, '//*[@id="the-post"]/div[1]/h3')
sleep(1)

data = []

for header in headers:
    driver.execute_script("arguments[0].scrollIntoView();", header)
    title = header.text
    next_element = header.find_element(By.XPATH, "following-sibling::p[1]")
    curiosity = next_element.text
    data.append({"Titulo": title, "Curiosidad": curiosity})
    sleep(1)

df = pd.DataFrame(data)
df.to_excel("docs/lostraveleros/lostravelos.xlsx", index=False)

sleep(1)

driver.quit()
