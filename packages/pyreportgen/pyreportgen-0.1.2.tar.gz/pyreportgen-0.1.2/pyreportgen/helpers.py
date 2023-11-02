import uuid
from pyreportgen.base import _DATA_DIR
import os

def clamp(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num

def random_path(filetype):
    return f"{_DATA_DIR}/{str(uuid.uuid4())}."+filetype

def to_html_path(path):
    return "file://"+str(os.path.abspath('index.html'))

def tagwrap(content:str, tag:str, classList="", props="") -> str:
    return f"<{tag} class='{classList}' {props}>{content}</{tag}>"