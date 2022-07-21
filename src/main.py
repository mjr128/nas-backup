import sys
import traceback
from ftp import Ftp
from Bdd import BDD
import config
import os.path
import datetime
import shutil
from Disk import Disk
from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ServerFile import ServerFile
from DiskFile import DiskFile

from Base import Base

folderToSave='/Raid/Livres_audio/Robert Jordan'

database = sys.argv[1]
database_user = sys.argv[2]
database_pw = sys.argv[3]
if(len(sys.argv) > 4):
    pathToCheck = sys.argv[4]
    prefixServerFolder = sys.argv[5]

database_str = 'mysql+mysqlconnector://'+database_user+':'+database_pw+'@'+database
print('database connection...')
print (database_str)
engine = create_engine(database_str, echo=False)
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
    print('ftp connection...')
    ftp = Ftp(config.host, config.port, config.user, config.pwd)
    ftp.connect()
    ftp.cd(folderToSave)
    print('ftp OK')

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
    ftp.disconnect()

def getDiskList():
    import win32api
    drives = []
    i=0
    for letter in win32api.GetLogicalDriveStrings().split('\x00')[:-1]:
        try:
            total, used, free = shutil.disk_usage(letter)
            name, partitionID, maxfilenamlen, sysflags, filesystemtype = win32api.GetVolumeInformation(letter)
            drives.append(Disk(letter, name, int(total/1024/1024/1024), int(used/1024/1024/1024), int(free/1024/1024/1024), partitionID))
        except Exception: 
            print('ERREUR')
        i=i+1
    return drives

def buildFilesList(path, diskName):
    print(path)
    finalFiles = []
    for root, dirs, files in os.walk(path):
        print(root)
        for file in files:
            fullPath = os.path.join(root, file)
            finalFiles.append( DiskFile( fullPath=fullPath , dirName=root, filename=file, size=os.stat(fullPath).st_size, diskName=diskName) )
    return finalFiles

def analyseHddData():
    disks = getDiskList()
    for disk in disks:
        print('\nDisque '+disk.name+' '+disk.letter+'\n'+
        'Taile: ' + str(disk.totalSize)+' Go ('+str(disk.freeSize)+' Go libres)\n'+
        'Partition ID: ' + str(disk.partitionID) +'\n')
    userInput = input('Choix du disque: ')
    choosenDisk = next(d for d in disks if d.letter[0] == userInput.upper())
    MAIN_DIR = ''
    rootDir = choosenDisk.letter+MAIN_DIR

    if not os.path.exists( rootDir ):
        print('creating save directory '+MAIN_DIR)
        os.mkdir(rootDir)

    files = buildFilesList(rootDir, choosenDisk.name)
    print(str(len(files))+' fichiers trouvés')
    fileInThisDisk = session.query( DiskFile ).filter( DiskFile.disk_name==choosenDisk.name )
    for f in fileInThisDisk:
        session.delete(f)
    for f in files:
        print(f.dir_name,f.filename, f.size)
        session.add(f)
    session.commit()

def analyseNasDataFromNas(path):
    print(path)
    finalFiles = []
    for root, dirs, files in os.walk(path):
        print(root)
        for file in files:
            realFullPath = os.path.join(root, file)
            #finalFiles.append( DiskFile( fullPath=realFullPath , dirName=root, filename=file, size=os.stat(realFullPath).st_size, diskName='diskName') )
            finalFiles.append( ServerFile( str(os.path.join(prefixServerFolder, file)) , prefixServerFolder, str(file), os.stat(realFullPath).st_size) )
    print(str(len(finalFiles))+ ' files found')
    connexion =engine.connect()
    for f in finalFiles:
        print(f.full_path)
        #session.add(f)
        try:
            connexion.execute("INSERT INTO "+ServerFile.__tablename__+" (server_file_id, full_path, dir_name, filename, size) VALUES ("+str(f.server_file_id)+",'"+ f.full_path.replace("'","\\'")+"','"+f.dir_name.replace("'","\\'")+"','"+f.filename.replace("'","\\'")+"',"+str(f.size)+")")
        #connexion.execute("INSERT INTO "+ServerFile.__tablename__+" (server_file_id, full_path, dir_name, filename, size, date_seen) VALUES ("+str(f.server_file_id)+",'"+ f.full_path.replace("'","\'")+"','"+f.dir_name.replace("'","\'")+"','"+f.filename.replace("'","\'")+"',"+f.size+","+str(f.date_seen)+")")
        except Exception as err:
            print("Erreur à la sauvegarde du fichier: "+f.full_path)
            traceback.print_exc()
    session.commit()
    print("Done")


if('pathToCheck' in globals()):
    print('checking '+pathToCheck)
    analyseNasDataFromNas(pathToCheck)
else:
    choix = input("""
    1 - Analyser les données sur le NAS
    2 - Analyser les données sur le disque dur
    3 - Lancer la copie du NAS vers le disque dur
    Choix: """)


    if( choix == '1' ):
        analyseNasData()
    if( choix == '2'):
        analyseHddData()
