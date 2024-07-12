from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd

opts = Options()

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

opts.add_argument(f"{user_agent=}")

opts.add_argument("--headless")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=opts
)

driver.get("https://www.airbnb.com/")

sleep(3)

titulos_anuncios = driver.find_elements(
    By.XPATH, '//div[@data-testid="listing-card-title"]'
)

titulos = [titulo.text for titulo in titulos_anuncios]

df = pd.DataFrame(titulos, columns=["Título"])

df.to_excel("titulos_Airbnb.xlsx", index=False)

driver.quit()
