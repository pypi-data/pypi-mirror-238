from pyreportgen.base import Component, _DATA_DIR
import matplotlib.pyplot as plt
import numpy as np
import pyreportgen.helpers as helpers
import uuid

class HBarPlot(Component):
    def __init__(self, lables, data, title="", xlabel=""):
        super().__init__()
        self.lables = lables
        self.data = data
        self.title = title
        self.xlabel = xlabel
        self.path = helpers.random_path("png")

    def render(self) -> str:
        fig, ax = plt.subplots()

        y_pos = np.arange(len(self.lables))


        ax.barh(y_pos, self.data, align='center')
        ax.set_yticks(y_pos, labels=self.lables)
        ax.invert_yaxis() 
        ax.set_xlabel(self.xlabel)
        ax.set_title(self.title)

        plt.savefig(self.path, dpi=150)

        return helpers.tagwrap("", "img", "HBarPlot", f'src="{self.path.lstrip(_DATA_DIR+"/")}"')
    
class Table(Component):
    def __init__(self, data: list[list[str]], headers: list[str]=[], footers: list[str]=[]):
        self.data: list[list[str]] = data
        self.headers: list[str] = headers
        self.footers: list[str] = footers
    
    def render(self) -> str:
        tablecontent = ""
        
        headcontent = helpers.tagwrap("".join(
            [helpers.tagwrap(str(i), "th") for i in self.headers]
        ), "tr")
        
        for row in self.data:
            tablecontent += helpers.tagwrap("".join(
                [helpers.tagwrap(str(i), "td") for i in row]
        ), "tr")

        footcontent = helpers.tagwrap("".join(
            [helpers.tagwrap(str(i), "td") for i in self.footers]
        ), "tr", "tfoot")
        if len(self.footers) == 0:
            footcontent = ""
        if len(self.headers) == 0:
            headcontent = ""

        return helpers.tagwrap(headcontent+tablecontent+footcontent, "table", "Table NoBreak")