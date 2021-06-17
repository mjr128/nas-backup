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
        self.ftps.prot_p()
        self.ftps.voidcmd('TYPE I')


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

    def buildFilesList(self, currentPath: str, folder: str):
        files = []
        #currentDir = path.path.rfind('/')]
        print('Before cd in '+ self.ftps.pwd())
        self.cd(folder)
        currentPath += folder 
        print('currently in '+ self.ftps.pwd())
        for file in self.ftps.nlst():
            self.ftps.voidcmd('TYPE I')
            try:
                files.append( (currentPath+'/'+file, self.ftps.size(file)) )
            except Exception as e:
                try:
                    files.extend(self.buildFilesList(currentPath, file))
                    self.cd('..')
                except Exception as ex:
                    print(ex)
        return files

    def disconnect(self):
        self.ftps.close()