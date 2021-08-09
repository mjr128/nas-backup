import datetime
class File:

    def __init__(self, path: str, size: int, uuid='', dateSaved = datetime.date.today(), needUpdate = 1):
        self.path = path
        self.size = size
        self.dateSaved = dateSaved
        self.uuid = uuid
        self.needUpdate = needUpdate = 1

    def __str__(self):
        return self.path+'\t'+str(self.size)

    def __eq__(self,b):
        return self.path == b.path and self.size == b.size
