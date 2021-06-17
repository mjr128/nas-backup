

class File:
    def __init__(self, path: str, size: int):
        self.path = path
        self.size = size

    def __str__(self):
        return self.path+'\t'+str(self.size)

    def __eq__(self,b):
        return self.path == b.path and self.size == b.size
