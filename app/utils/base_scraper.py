# app/utils/scraper.py


from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from config.env import Env
from time import sleep


class BaseScraper:
    def __init__(self, headless=False):
        self.env = Env()
        self.opts = Options()
        self.opts.add_argument(f"user-agent={self.env.getEnv('USER_AGENT')}")
        self.opts.add_argument("--start-maximized")
        self.opts.add_argument("--disable-extensions")
        self.opts.add_argument("--no-sandbox")
        if headless:
            self.opts.add_argument("--headless")
        self.driver = webdriver.Chrome(service=ChromeService(), options=self.opts)
        self.by = {
            "XPATH": By.XPATH,
            "TAG_NAME": By.TAG_NAME,
        }

    def getBy(self, byName: str = "XPATH" or "TAG_NAME"):
        return self.by[byName.upper()]

    def getPage(self, url):
        self.driver.get(url)
        self.wait(5)

    def find(self, by, value, onlyElement=True):
        return (
            self.driver.find_element(by, value)
            if onlyElement
            else self.driver.find_elements(by, value)
        )

    def scrollIntoView(self, element):
        script = "arguments[0].scrollIntoView();"
        self.driver.execute_script(script, element)
        self.wait(1)

    def quit(self):
        self.driver.quit()

    def wait(self, seconds):
        sleep(seconds)

    def select(self, element, value):
        dropdown = Select(element)
        dropdown.select_by_visible_text(value)
        self.wait(3)

    def insertInput(self, element, value):
        element.send_keys(value)
        self.wait(1)
