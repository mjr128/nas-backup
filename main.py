from ftp import Ftp
import config

ftp = Ftp(config.host, config.port, config.user, config.pwd)
ftp.connect()
ftp.cd('/Raid/Livres_audio/Robert Jordan')

for f in ftp.buildFilesList():
    print(f)

ftp.disconnect()
