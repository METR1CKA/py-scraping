# app/utils/scraper.py


from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from config.env import Env


class BaseScraper:
    def __init__(self, headless=False):
        self.env = Env()
        self.opts = Options()
        self.opts.add_argument(f"user-agent={self.env.getEnv('USER_AGENT')}")
        self.opts.add_argument("--start-maximized")
        self.opts.add_argument("--disable-extensions")
        if headless:
            self.opts.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.opts
        )
        self.by = {
            "ID": By.ID,
            "NAME": By.NAME,
            "LINK": By.LINK_TEXT,
            "XPATH": By.XPATH,
        }

    def getBy(self):
        return self.by

    def getPage(self, url):
        self.driver.get(url)

    def findElements(self, byName, value):
        return self.driver.find_elements(self.by[byName], value)

    def quit(self):
        self.driver.quit()
