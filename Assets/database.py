import sqlite3


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('bot.db')

    def query(self, sql):
        print(sql)
        self.cur = self.connection.cursor()
        res = self.cur.execute(sql)
        self.connection.commit()
        return res

    def close(self):
        self.cur.close()
