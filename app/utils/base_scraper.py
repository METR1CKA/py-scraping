# app/base_scraper.py


from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from app.utils.pandas_df import PandasDataFrame
from selenium.webdriver.common.by import By
from selenium import webdriver
from config.env import Env
import time


class BaseScraper:
    def __init__(self, headless=False, env=False):
        self.opts = Options()
        if env:
            self.env = Env()
            self.opts.add_argument(f"user-agent={self.env.getEnv('USER_AGENT')}")
        if headless:
            self.opts.add_argument("--headless")
        self.opts.add_argument("--start-maximized")
        self.opts.add_argument("--disable-extensions")
        self.opts.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=ChromeService(), options=self.opts)
        self.processed_data = []
        self.BY_TYPES = {
            "XPATH": By.XPATH,
            "TAG_NAME": By.TAG_NAME,
        }
        self.commonActions = {
            "GET": self.GET,
            "SEND_KEYS": self.SEND_KEYS,
            "CLICK": self.CLICK,
            "SCROLL": self.SCROLL,
            "ELEMENTS": self.ELEMENTS,
            "SAVE-EXCEL": self.SAVE_EXCEL,
        }

    def getByTyped(self, byName):
        return self.BY_TYPES[byName.upper()]

    def getElement(self, by, value):
        return self.driver.find_element(by, value)

    def getElements(self, by, value):
        return self.driver.find_elements(by, value)

    def scrollIntoView(self, element):
        script = "arguments[0].scrollIntoView();"
        self.driver.execute_script(script, element)

    def scrollTop(self):
        script = "window.scrollTo(0, 0);"
        self.driver.execute_script(script)

    def webWait(self, seconds):
        return WebDriverWait(self.driver, seconds, 1)

    def waitTime(self, seconds=None):
        time.sleep(seconds if seconds else 1)

    def select(self, element, value):
        dropdown = Select(element)
        dropdown.select_by_visible_text(value)

    def insertInput(self, element, value):
        element.send_keys(value)

    def quit(self):
        self.driver.quit()

    def setData(self, data):
        self.data = data

    def setProperties(self):
        by, selector, keys, time, scroll = (
            self.data.get("by"),
            self.data.get("selector"),
            self.data.get("keys"),
            self.data.get("time"),
            self.data.get("scroll"),
        )
        self.by = self.getByTyped(by)
        self.selector = selector
        self.keys = keys
        self.time = time
        self.scroll = scroll

    def GET(self):
        self.driver.get(self.data.get("url"))
        self.waitTime(self.data.get("time"))

    def SEND_KEYS(self):
        self.setProperties()
        element = self.getElement(self.by, self.selector)
        self.waitTime(self.time)
        element.send_keys(self.keys)
        self.waitTime(self.time)

    def CLICK(self):
        self.setProperties()
        element = self.getElement(self.by, self.selector)
        if self.scroll:
            self.scrollIntoView(element)
        element.click()
        self.waitTime(self.time)

    def SCROLL(self):
        self.setProperties()
        element = self.getElement(self.by, self.selector)
        if self.scroll:
            self.scrollIntoView(element)
        self.waitTime(self.time)

    def ELEMENTS(self):
        self.setProperties()
        elements = self.getElements(self.by, self.selector)
        self.waitTime(self.time)
        self.elements = elements

    def SAVE_EXCEL(self):
        pandas = PandasDataFrame()
        df = pandas.createDataFrame(self.elements)
        pandas.exportToExcel(
            data=df, folders=self.data.get("paths"), filename=self.data.get("filename")
        )
