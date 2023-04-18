import mysql.connector

class Data:
    def __init__(self):
        self._db = mysql.connector.connect(user='root',passwd='123456',database='Game')
        self._cursor = self._db.cursor()

    def insert(self, score, datetime):
        sql = "INSERT INTO record (score,record_date) VALUES(%s,%s)"
        val = (score,datetime)
        self._cursor.execute(sql,val)
        self._db.commit()

    def select(self):
        sql = "SELECT score, record_date FROM record ORDER BY id DESC LIMIT 5"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        return list(result)
    
    def selectHighestScore(self):
        sql = "SELECT score, record_date FROM record WHERE score = (SELECT MAX(score) FROM record)"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        return result
