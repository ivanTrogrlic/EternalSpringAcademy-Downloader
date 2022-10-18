import re
import sqlite3 as sl
import string
from tokenize import String

from file_utils import *

OBJAVE = "Objave"

class Database:
    def __init__(self):
        self.con = sl.connect('objave.db')
        self.create_table()

    def create_table(self):
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS OBJAVA (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                number INTEGER,
                title TEXT,
                subtitle TEXT,
                filename TEXT,
                favourite INTEGER
            );
        """)
    
    def insert_objava(self, objava_html: string, filename: string):
        objavaMatch = re.search("(?=<div class=\"okvir\">)([\S\s]*?)(?<=<\/div>)", objava_html)
        objava = str(objavaMatch.group())
        subtitleMatch = re.search("(?=Bertha([\S\s]*)Dudde)([\S\s]*?)(?=<\/span>)", objava)
        titleMatch = re.search("(?<=<title>)([\S\s]*?)(?=<\/title>)", objava_html)
        
        subtitle = str(subtitleMatch.group())
        title = str(titleMatch.group())
        number = int(title[12:16])

        print(title)
        print(subtitle)
        print(number)

        sql = 'INSERT INTO OBJAVA (number, title, subtitle, filename, favourite) values(?, ?, ?, ?, ?)'
        data = (number, title, subtitle, filename, 0)

        write_file(OBJAVE + "/" + filename + ".txt", objava)
        self.con.execute(sql, data)
        self.con.commit()
        print("Saved to database")
