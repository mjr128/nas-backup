from ftp import Ftp
from Bdd import BDD
import config
import os.path
from os import path

ftp = Ftp(config.host, config.port, config.user, config.pwd)
ftp.connect()
ftp.cd('/Raid/Livres_audio/Robert Jordan')

bdd = BDD('nas-backup')
bdd.connect()
bdd.init()

for f in ftp.buildFilesList():
    print(f)
    localPath = './save'+f.path
    fileInDb = bdd.get(f.path)
    if (not path.exists(localPath)) or os.stat(localPath).st_size != f.size:
        try:
            os.makedirs(os.path.dirname(localPath))
        except FileExistsError as e:
            e
        print('downloading...')
        ftp.download(localPath, '/Raid/Livres_audio/Robert Jordan'+f.path)
        bdd.insert(f)
    else:
        f.needUpdate = 0
        bdd.insert(f)
    print('OK')


ftp.disconnect()
