from pyreportgen import Component


class HBox(Component):
    def __init__(self, children=[]):
        super().__init__()
        self.children = children
    
    def render(self) -> str:
        html = ""

        for i in self.children:
            html += i.render()

        

        return f"""
            <div class="HBox">
                {html}
            </div>

"""
    
class VBox(Component):
    def __init__(self, children=[]):
        super().__init__()
        self.children = children
    
    def render(self) -> str:
        html = ""

        for i in self.children:
            html += i.render()

        

        return f"""
            <div class="VBox NoBreak">
                {html}
            </div>

"""
    
class HCenterContent(Component):
    def __init__(self, child:Component):
        super().__init__()
        self.child = child
    def render(self) -> str:
        return f"""<div class="HCenterContent">{self.child.render()}</div>"""