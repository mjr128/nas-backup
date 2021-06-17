from ftp import Ftp
import ftputil
import config

ftp = Ftp(config.host, config.port, config.user, config.pwd)
ftp.connect()
#ftp.cd('Raid/mjr128')
#ftp.cd('mjr128')
ftp.ls()
s = ftp.buildFilesList('/', 'Raid/Series/Californication/')
print(s)

#ftp.download('rarlinux-x64-5.9.1.tar')
#ftp.download('')
#ftp.test()
ftp.disconnect()
