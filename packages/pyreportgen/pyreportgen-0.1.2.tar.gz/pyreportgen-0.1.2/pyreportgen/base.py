
_DATA_DIR = ".pyreportgen_data"


class Component:
    def __init__(self):
        pass

    def render(self) -> str:
        print(f"Component {self} has no renderer.")
        return f"""<p style='color: red'>Component {self.__repr__().replace("<", "&lt;").replace(">", "&gt;")} has no renderer</p>"""