from charset_normalizer import from_path
from .File import File

class TextFile(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__set_encoding()

    @property
    def encoding(self) -> str:
        return self.attributes.get("encoding")

    @encoding.setter
    def encoding(self, value:str):
        self.attributes["encoding"] = value

    def __set_encoding(self):
        result = from_path(self.attributes.get("full_path")).best()
        self.encoding = result.encoding
    
    def to_string(self, size: str) -> str:
        return f"{self.name}{self.extension} [純文字檔] (編碼: {self.encoding}, 大小: {size})"

    def to_xml(self, size: str) -> str:
        return f"<{self.name}_{self.extension[1:]}> 編碼:{self.encoding}, 大小:{size} </{self.name}_{self.extension[1:]}>"