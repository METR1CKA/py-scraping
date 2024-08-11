# app/classes/kingsleague.py


from app.utils.pandas_df import PandasDataFrame


class KingsLeague:
    def __init__(self, scraper):
        self.scraper = scraper
        self.pandas = PandasDataFrame()

    def splits(self):
        # Obtener la información de los splits
        self.scraper.setProperties()
        original_data = self.scraper.data
        split_indexes = original_data.get("indexes")
        paths = original_data.get("paths")
        filename = original_data.get("filename")
        time = original_data.get("time")
        selector1 = self.scraper.selector.get("value-1")
        selector2 = self.scraper.selector.get("value-2")
        self.scraper.waitTime(time)
        # Iterar sobre los splits
        for i, split_index in enumerate(split_indexes):
            element = self.scraper.getElement(
                self.scraper.by, selector1.replace(":index", str(split_index))
            )
            element.click()
            self.scraper.waitTime(time)
            elements = self.scraper.getElements(self.scraper.by, selector2)
            headers = []
            data = []
            header_div = elements[0]
            header_texts = header_div.text.split("\n")
            headers = header_texts
            for element in elements[1:]:
                text_list = element.text.split("\n")
                data.append(text_list)
            df = self.pandas.createDataFrame(data, headers)
            self.pandas.exportToExcel(
                data=df, folders=paths, filename=filename.replace(":index", str(i + 1))
            )

    def cups(self):
        # Obtener la información de los splits
        self.scraper.setProperties()
        original_data = self.scraper.data
        cup_indexes = original_data.get("indexes")
        paths = original_data.get("paths")
        time = original_data.get("time")
        selector1 = self.scraper.selector.get("value-1")
        selector2 = self.scraper.selector.get("value-2")
        selector3 = self.scraper.selector.get("value-3")
        selector4 = self.scraper.selector.get("value-4")
        self.scraper.waitTime(time)
        for cup_index in cup_indexes:
            element = self.scraper.getElement(
                self.scraper.by, selector1.replace(":index", str(cup_index))
            )
            element.click()
            self.scraper.waitTime(time)
            elements = self.scraper.getElements(self.scraper.by, selector2)
            folders = paths.get("folders")
            if len(folders) == 3:
                folders.pop()
            if cup_index == 3:
                folders.append(paths.get("kings_cup"))
            if cup_index == 4:
                folders.append(paths.get("kingdom_cup"))
            for sub_element in elements:
                group_element = sub_element.find_element(self.scraper.by, selector3)
                group_split = group_element.text.split("\n")
                group = "_".join(group_split)
                table_elements = sub_element.find_elements(self.scraper.by, selector4)
                headers = []
                data = []
                header_div = table_elements[0]
                header_texts = header_div.text.split("\n")
                headers = header_texts
                for element in table_elements[1:]:
                    text_list = element.text.split("\n")
                    data.append(text_list)
                df = self.pandas.createDataFrame(data, headers)
                self.pandas.exportToExcel(data=df, folders=folders, filename=group)
