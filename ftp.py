from ftplib import FTP_TLS

class Ftp :

    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.ftps = FTP_TLS()

    def connect(self):
        self.ftps.connect(self.host, self.port)
        self.ftps.login(self.user, self.pwd)
        s = self.ftps.prot_p()


    def test(self):
        s = self.ftps.retrlines('LIST')
        print(s)
        s = self.ftps.cwd('Raid')
        print(s)
        s = self.ftps.dir()
        print(s)

    def cd(self, dir):
        s = self.ftps.cwd(dir)
        print(s)

    def ls(self):
        s = self.ftps.retrlines('LIST')
        print(s)

    def download(self, filename):
        #handle = open(path.rstrip("/") + "/" + filename.lstrip("/"), 'wb')
        handle = open(filename, 'wb')
        self.ftps.retrbinary('RETR %s' % filename, handle.write)
        handle.close()

    def buildFilesList(self, ):
        self.ftps.

    def disconnect(self):
        self.ftps.close()