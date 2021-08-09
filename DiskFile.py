#!/usr/bin/python3

from sqlalchemy import Column, Integer, Text, DateTime, Boolean

import datetime
from Base import Base

# Definition of the Contact class
class DiskFile( Base ):
    __tablename__ = 'DISK_FILES'

    disk_file_id = Column(Integer, primary_key=True)
    full_path = Column(Text)
    dir_name = Column(Text)
    filename = Column(Text)
    disk_uuid = Column(Text)
    size = Column(Integer)
    date_save = Column(DateTime)
    date_seen = Column(DateTime)
    needUpdate = Column(Boolean)

    def __init__(self, fullPath, dirName, filename, size, dateSeen = datetime.date.today()):
        self.full_path = fullPath
        self.dir_name = dirName
        self.filename = filename
        self.size = size
        self.date_seen = dateSeen 
        self.needUpdate = 1

    def __str__(self):
        return self.fullPath