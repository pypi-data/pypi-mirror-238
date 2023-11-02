import re
import os
import matplotlib
import pyreportgen.style as style
import pyreportgen.layout as layout
import pyreportgen.helpers as helpers
import pyreportgen.statistic as statistic
from pyreportgen.base import Component, _DATA_DIR



if not (_DATA_DIR in os.listdir()):
    os.makedirs(_DATA_DIR, exist_ok=True)


_RE_COMBINE_WHITESPACE = re.compile(r"\s+")



class Report(Component):
    def __init__(self, children=[], style:str=style.STYLE_NORMAL):
        super().__init__()
        self.children = children
        self.style = style

    def render(self) -> str:
        html = ""
        for i in self.children:
            html += i.render()
        html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>{self.style}</style>
                <title>Report</title>
            </head>
            <body>
                <main class="Main">
                    {html}
                <main>
            </body>
        """

        return _RE_COMBINE_WHITESPACE.sub(" ", html).strip()
    
    def pdf(self, path:str):
        import pdfkit 
        html = self.render()
        with open(_DATA_DIR+'/out.html', 'w', encoding="UTF-8") as f:
            f.write(html)

        pdfkit.from_file(_DATA_DIR+'/out.html', path, options={"--enable-local-file-access":None, "--print-media-type":None}) 

class Html(Component):
    def __init__(self, html):
        super().__init__()
        self.html = html
    def render(self) -> str:
        return self.html

class Text(Component):
    element = "p"

    def __init__(self, text, center=False):
        super().__init__()
        self.text = text
        self.center = center
    
    def render(self) -> str:
        classlist = ""
        if self.center:
            classlist += "CenterText "

        return helpers.tagwrap(self.text, self.element, classList=classlist)

class Header(Text):
    def __init__(self, text, center=True, heading=1):
        super().__init__(text, center)
        self.element = "h"+str(helpers.clamp(heading, 1, 6))
    
    def render(self) -> str:
        return super().render()

class Image(Component):
    def __init__(self, src):
        super().__init__()
        self.src = src
    
    def render(self) -> str:
        return helpers.tagwrap("", "img", "Image", f"src='../{self.src}'")
