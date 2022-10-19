import re
import sqlite3 as sl
import string
import html
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
                number INTEGER NOT NULL PRIMARY KEY,
                title TEXT NOT NULL,
                subtitle TEXT NOT NULL,
                filename TEXT NOT NULL,
                favourite INTEGER NOT NULL
            );
        """)
    
    def insert_objava(self, objava_html: string, filename: string):
        # First dig out the required data from the HTML string via regex. 
        objavaMatch = re.search("(?=<div class=\"okvir\">)([\S\s]*?)(?<=<\/div>)", objava_html)
        objava = str(objavaMatch.group())
        subtitleMatch = re.search("(?=Bertha)([\S\s]*?)(?=<\/)", objava)
        titleMatch = re.search("(?<=<title>)([\S\s]*?)(?=<\/title>)", objava_html)
        
        subtitle = str(subtitleMatch.group())
        title = str(titleMatch.group())

        # Unescape HTML encoded characters.
        subtitleUnescaped = html.unescape(subtitle)
        titleUnescaped = html.unescape(title)

        # Remove extra whitespaces, tabs, newlines..
        subtitleFixed = re.sub('\s+',' ',subtitleUnescaped)

        # Get the number from subtitle, where prefix is always 'Bertha Dudde, br. ' followed by 4 characters integer.
        number = int(subtitleFixed[18:22])

        write_file(OBJAVE + "/" + filename + ".txt", objava)

        sql = 'INSERT INTO OBJAVA (number, title, subtitle, filename, favourite) values(?, ?, ?, ?, ?)'
        data = (number, titleUnescaped, subtitleFixed, filename, 0)
        self.con.execute(sql, data)
        self.con.commit()

        print("Saved to database")
