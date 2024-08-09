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
    title = header.text
    next_element = header.find_element(By.XPATH, "following-sibling::p[1]")
    curiosity = next_element.text
    data.append({"Titulo": title, "Curiosidad": curiosity})

df = pd.DataFrame(data)
df.to_excel("docs/lostraveleros/lostravelos.xlsx", index=False)

sleep(1)

driver.quit()
