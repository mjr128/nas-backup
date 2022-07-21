import sqlite3
from File import File

class BDD:
    def __init__(self, dbName):
        self.dbName = dbName
    
    def connect(self):
        self.conn = sqlite3.connect(self.dbName)

    def init(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS FILES(
                server_path TEXT PRIMARY KEY,
                disk_uuid TEXT,
                size INTEGER,
                date_save DATE,
                needUpdate INTEGER DEFAULT 1
            )
        """)
    
    def insert(self, f: File):
        if not self.cursor:
            self.cursor = self.conn.cursor()
        self.cursor.execute("""
            INSERT INTO FILES(server_path, disk_uuid, size, date_save)
            VALUES (:path, :uuid, :size, :dateSaved)
        """, f)

    def get(self, serverPath):
        self.cursor.execute("""
            SELECT server_path, size, disk_uuid, date_save FROM FILES WHERE server_path = ?
        """, (serverPath,))
        rows = self.cursor.fetchall()
        files = []
        for row in rows:
            files.append(File(row[0], row[1], row[2], row[3]))
        return files

