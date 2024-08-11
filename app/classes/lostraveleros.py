# app/classes/lostraveleros.py


from app.utils.pandas_df import PandasDataFrame


class LosTraveleros:
    def __init__(self, scraper):
        self.scraper = scraper
        self.pandas = PandasDataFrame()

    def extractTableDivs(self):
        self.scraper.setProperties()
        headers_xpath = self.scraper.selector.get("headers")
        next_element_xpath = self.scraper.selector.get("next_element")
        headers = self.scraper.getElements(self.scraper.by, headers_xpath)
        self.scraper.waitTime(self.scraper.time)
        data = []
        for header in headers:
            self.scraper.scrollIntoView(header)
            title = header.text
            next_element = header.find_element(self.scraper.by, next_element_xpath)
            curiosity = next_element.text
            data.append({"Titulo": title, "Curiosidad": curiosity})
            self.scraper.waitTime(self.scraper.time)
        df = self.pandas.createDataFrame(data)
        self.pandas.exportToExcel(
            data=df,
            folders=self.scraper.data.get("paths"),
            filename=self.scraper.data.get("filename"),
        )
