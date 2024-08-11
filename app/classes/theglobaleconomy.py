# app/classes/theglobaleconomy.py


from app.utils.pandas_df import PandasDataFrame


class TheGlobalEconomy:
    def __init__(self, scraper):
        self.scraper = scraper
        self.pandas = PandasDataFrame()

    def extractTable(self):
        type_selector, selectors = (
            self.scraper.data.get("type-selector"),
            self.scraper.data.get("selectors"),
        )
        headers_rows_by, cols_by = (
            type_selector.get("headers-rows"),
            type_selector.get("cols"),
        )
        headers_selector, rows_selector, cols_selector = (
            selectors.get("headers"),
            selectors.get("rows"),
            selectors.get("cols"),
        )
        headers_rows_by = self.scraper.getByTyped(headers_rows_by)
        cols_by = self.scraper.getByTyped(cols_by)
        headers = self.scraper.getElements(headers_rows_by, headers_selector)
        headers = [header.text for header in headers]
        rows = self.scraper.getElements(headers_rows_by, rows_selector)
        data = []
        for row in rows:
            cols = row.find_elements(cols_by, cols_selector)
            cols = [col.text for col in cols]
            data.append(cols)
        df = self.pandas.createDataFrame(data, headers)
        self.pandas.exportToExcel(
            data=df,
            folders=self.scraper.data.get("paths"),
            filename=self.scraper.data.get("filename"),
        )
        self.scraper.waitTime(self.scraper.data.get("time"))
