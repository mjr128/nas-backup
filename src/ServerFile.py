#!/usr/bin/python3

from sqlalchemy import BIGINT, create_engine, ForeignKey, func
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, VARCHAR
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime
from Base import Base

# Definition of the Contact class
class ServerFile( Base ):
    __tablename__ = 'SERVER_FILES'
    server_file_id = Column(BIGINT, primary_key=True, autoincrement = False )
    full_path = Column(VARCHAR(512))
    dir_name = Column(Text)
    filename = Column(Text)
    size = Column(BIGINT)
    date_seen = Column(DateTime, server_default=func.now())

    def __init__(self, fullPath, dirName, filename, size, dateSeen = datetime.date.today()):
        self.server_file_id = hash(fullPath)
        self.full_path = fullPath
        self.dir_name = dirName
        self.filename = filename
        self.size = size
        self.date_seen = dateSeen

    #def __str__(self):
    #    return self.full_path

    #def __eq__(self, o):
    #    return self.full_path == o.full_path

    #def updateFrom(self, o):
    #    assert self.full_path == o.full_path
    #    assert self.dir_name == o.dir_name
    #    assert self.filename == o.filename

    #    self.size = o.size
    #    self.date_save = o.date_save
    #    self.date_seen = o.date_seen
    #    self.disk_file_id = o.disk_file_id