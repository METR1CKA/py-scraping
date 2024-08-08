# app/models/airbnb.py

from selenium.webdriver.common.by import By
import sys, os

# sys.path.append(
#     os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# )

from app.utils.pandas_df import PandasDataFrame
from app.utils.base_scraper import BaseScraper

# from config.jsonConfig import JsonConfig


class AirbnbScraper(BaseScraper):
    def __init__(self):
        super().__init__()

    def main(self):
        pass


if __name__ == "__main__":
    airbnb = AirbnbScraper()
    airbnb.main()
