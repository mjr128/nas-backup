from ftp import Ftp
from Bdd import BDD
import config
import os.path
import datetime
import win32api
import shutil
from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ServerFile import ServerFile
from DiskFile import DiskFile

from Base import Base

folderToSave='/Raid/Livres_audio/Robert Jordan'

print('ftp connection...')
ftp = Ftp(config.host, config.port, config.user, config.pwd)
ftp.connect()
ftp.cd(folderToSave)
print('ftp OK')

print('database connection...')
engine = create_engine('mysql+mysqlconnector://root@localhost/nas-db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
ee = session.query( ServerFile ).get(1)
print('db OK')

def downloadFolder():
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

def printFolderContent():
    for (foldername, files) in ftp.buildFilesListByFolder():
        otherInDir = session.query( ServerFile ).filter( ServerFile.dir_name==foldername ).filter( ~ServerFile.filename.in_([f.filename for f in files]) ).all()
        inDB = session.query( ServerFile ).filter( ServerFile.full_path.in_([f.full_path for f in files]) ).all()

        print(foldername)
        print(len(otherInDir))
        print(len(inDB))

        for file in otherInDir:
            print('deleting '+str(file))
            session.delete(file)
        
        for file in files:
            session.save(file)
        session.commit()

def analyseNasData():
    print('Building file list...')
    nasFiles = ftp.buildFilesList(folderToSave)
    print('found '+str(len(nasFiles))+' files')
    print('Backup current database...')
    connexion = engine.connect()
    connexion.execute('CREATE TABLE IF NOT EXISTS '+ServerFile.__tablename__+'_'+datetime.date.today().strftime('%Y_%m_%d')+' SELECT * FROM '+ServerFile.__tablename__)
    #print('Drop current database...')
    #connexion.execute('TRUNCATE TABLE '+ServerFile.__tablename__)
    print('Saving data in database...')
    for nasFile in nasFiles:
        savedEntity = session.query( ServerFile ).outerjoin( DiskFile ).filter( ServerFile.full_path==nasFile.full_path ).first()
        if( savedEntity ):
            if( savedEntity.diskFile and savedEntity.diskFile.size == nasFile.size and savedEntity.size == nasFile.size ):
                savedEntity.needUpdate = 0
            else:
                savedEntity.updateFrom(nasFile)
        else:
            session.add( nasFile )
    print('Deleting old data in database...')
    oldFiles = session.query( ServerFile ).filter( ~ServerFile.full_path.in_([f.full_path for f in nasFiles]))
    print('deleting '+str(len(oldFiles)))
    for f in oldFiles:
        session.delete(f)
    session.commit()
    print('Done')

def analyseHddData():
    drives = []
    for letter in win32api.GetLogicalDriveStrings().split('\x00')[:-1]:
        total, used, free = shutil.disk_usage(letter)
        drives.append((letter, win32api.GetVolumeInformation(letter)[0], str(int(total/1024/1024/1024))+'Go', str(int(used/1024/1024/1024))+'Go', str(int(free/1024/1024/1024))+'Go'))
    
    input('Choix du disque\n'+ )


choix = input("""
1 - Analyser les données sur le NAS
2 - Analyser les données sur le disque dur
3 - Lancer la copie du NAS vers le disque dur
Choix: """)

#if( choix == '1' ):
#    analyseNasData()
#if( choix == '2'):
analyseHddData()

ftp.disconnect()
