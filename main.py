from ftp import Ftp
from Bdd import BDD
import config
import os.path
from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ServerFile import ServerFile
from DiskFile import DiskFile

from Base import Base

ftp = Ftp(config.host, config.port, config.user, config.pwd)
ftp.connect()
ftp.cd('/Raid/Livres_audio/Robert Jordan')

engine = create_engine('mysql+mysqlconnector://root@localhost/nas-db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
ee = session.query( ServerFile ).get(1)
print('db OK')

for f in ftp.buildFilesList():
    print(f)
    localPath = './save'+f.path
    if (not path.exists(localPath)) or os.stat(localPath).st_size != f.size:
        try:
            os.makedirs(os.path.dirname(localPath))
        except FileExistsError as e:
            e
        print('downloading...')
        ftp.download(localPath, '/Raid/Livres_audio/Robert Jordan'+f.path)
    else:
        f.needUpdate = 0
    print('OK')


ftp.disconnect()
