from importlib.resources import path
from PIL import Image
from .File import File

class ImageFile(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__set_resolution()

    @property
    def width(self) -> int:
        return self.attributes.get("width")

    @width.setter
    def width(self, value:int):
        self.attributes["width"] = value

    @property
    def height(self) -> int:
        return self.attributes.get("height")

    @height.setter
    def height(self, value:int):
        self.attributes["height"] = value

    def __set_resolution(self):
        path = self.attributes.get("full_path")
        if path is None:
            return
        with Image.open(path) as img:
            self.width = img.width
            self.height = img.height
    
    def to_string(self, size: str) -> str:
        return f"{self.name}{self.extension} [圖片檔] (解析度: {self.width}x{self.height}, 大小: {size})"

    def to_xml(self, size: str) -> str:
        return f"<{self.name}_{self.extension[1:]}> 解析度:{self.width}x{self.height}, 大小:{size} </{self.name}_{self.extension[1:]}>"