import uuid
import os

def clamp(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num

def random_path(filetype):
    return f".pyreportgen_data/{str(uuid.uuid4())}."+filetype

def to_html_path(path):
    return "file://"+str(os.path.abspath('index.html'))