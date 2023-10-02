from mysql.connector import Error
import mysql.connector


class ConnectDB:
    def __init__(self, host="localhost", port="3306", database="studio_beard", user="root", password="root"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def conecta(self):
        self.con = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cur = self.con.cursor(dictionary=True)

    def commit(self):
        self.con.commit()

    def rollback(self):
        self.con.rollback()

    def execute(self, query, data=''):
        self.cur.execute(query, data)
        # print("Results: ", affected_count)
        affected_count = self.cur.rowcount
        return affected_count

    def desconecta(self):
        self.con.close()

    def fetchall(self):
        return self.cur.fetchall()

    def fetchone(self):
        return self.cur.fetchone()


if __name__ == "__main__":
    conn = ConnectDB()
    conn.conecta()
    sql = "select * from clientes"
    conn.execute(sql)
    t = conn.fetchone()
    print(t)

