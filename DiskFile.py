#!/usr/bin/python3

from sqlalchemy import BIGINT, Column, Integer, Text, DateTime, Boolean, null

import datetime
from Base import Base

# Definition of the Contact class
class DiskFile( Base ):
    __tablename__ = 'DISK_FILES'

    disk_file_id = Column(Integer, primary_key=True)
    full_path = Column(Text)
    dir_name = Column(Text)
    filename = Column(Text)
    disk_name = Column(Text)
    size = Column(BIGINT)
    #date_save = Column(DateTime)
    date_seen = Column(DateTime)
    needUpdate = Column(Boolean)

    def __init__(self, fullPath, dirName, filename, size, diskName, dateSeen = datetime.date.today()):
        self.disk_file_id = hash(fullPath)
        self.full_path = fullPath
        self.dir_name = dirName
        self.filename = filename
        self.disk_name = diskName
        self.size = size
        #self.date_save = null
        self.date_seen = dateSeen 
        self.needUpdate = 1

    def __str__(self):
        return self.fullPath