from File.File import File

class Directory:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.files = []

    def add_file(self, file: File):
        self.files.append(file)

    def add_directory(self, directory: "Directory"):
        self.children.append(directory)