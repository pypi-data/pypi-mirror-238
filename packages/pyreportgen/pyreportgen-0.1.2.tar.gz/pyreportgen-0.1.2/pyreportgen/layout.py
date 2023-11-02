
from pyreportgen.base import Component
import pyreportgen.helpers as helpers 


class HBox(Component):
    def __init__(self, children=[]):
        super().__init__()
        self.children = children
    
    def render(self) -> str:
        html = ""

        for i in self.children:
            html += i.render()

        
        return helpers.tagwrap(html, "div", "HBox")

    
class VBox(Component):
    def __init__(self, children=[]):
        super().__init__()
        self.children = children
    
    def render(self) -> str:
        html = ""

        for i in self.children:
            html += i.render()

        return helpers.tagwrap(html, "div", "VBox NoBreak")
    
class HCenterContent(Component):
    def __init__(self, child:Component):
        super().__init__()
        self.child = child
    def render(self) -> str:
        return helpers.tagwrap(self.child.render(), "div", "HCenterContent")
    
class PageBreak(Component):
    def __init__(self):
        super().__init__()
    
    def render(self) -> str:
        return helpers.tagwrap("", "div", "PageBreak")
    
class List(Component):
    def __init__(self, elements:list[str]):
        super().__init__()
        self.elements = elements

    def render(self) -> str:
        html = ""
        for el in self.elements:
            html += helpers.tagwrap(el, "li")
        
        return helpers.tagwrap(html, "ul")