from ftp import Ftp

import config

ftp = Ftp(config.host, config.port, config.user, config.pwd)
ftp.connect()
ftp.test()
ftp.disconnect()
