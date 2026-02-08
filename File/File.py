from abc import abstractmethod


class File:
    def __init__(self, **kwargs):
        self.attributes = kwargs

    @property
    def name(self) -> str:
        return self.attributes.get("name")
    
    @name.setter
    def name(self, value:str):
        self.attributes["name"] = value

    @property
    def extension(self) -> str:
        return self.attributes.get("extension")

    @extension.setter
    def extension(self, value:str):
        self.attributes["extension"] = value

    @property
    def size(self) -> int:
        return self.attributes.get("size")

    @size.setter
    def size(self, value:float):
        self.attributes["size"] = value

    @property
    def createdTime(self) -> str:
        return self.attributes.get("createdTime")

    @createdTime.setter
    def createdTime(self, value:str):
        self.attributes["createdTime"] = value

    @abstractmethod
    def to_string(self, size: str) -> str:
        pass

    @abstractmethod
    def to_xml(self, size: str) -> str:
        pass
