# app/utils/pandas_df.py


from config.app import App
import pandas as pd


class PandasDataFrame:
    def __init__(self, folder="docs"):
        self.app = App()
        self.docs = folder
        self.docsDir = self.app.joinPaths(folder)

    def createDataFrame(self, data, headers: list[str] | None):
        return (
            pd.DataFrame(data, columns=headers)
            if headers is not None
            else pd.DataFrame(data)
        )

    def exportToExcel(self, data: pd.DataFrame, folders: list, filename: str):
        fullFolderPath = self.app.joinPaths(self.docsDir, *folders)
        if not self.app.exists(fullFolderPath):
            self.app.makeDirs(fullFolderPath)
        path = self.app.joinPaths(fullFolderPath, f"{filename}.xlsx")
        data.to_excel(path, index=False)
        return self.app.joinPaths(".", self.docs, *folders, f"{filename}.xlsx")
