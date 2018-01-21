import mysql.connector

USER_NAME = 'DbMysql04'
PASSWORD = 'DbMysql04'
DB = 'DbMysql04'
HOST = 'mysqlsrv.cs.tau.ac.il'


def run_get_query(query):
    nx = mysql.connector.connect(host=HOST, user=USER_NAME, password=PASSWORD, database=DB)
    cursor = nx.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    nx.close()

    return rows


def run_and_commit_query(query):
    nx = mysql.connector.connect(host=HOST, user=USER_NAME, password=PASSWORD, database=DB)
    cursor = nx.cursor(dictionary=True)
    cursor.execute(query)
    nx.commit()
    id = cursor.lastrowid
    cursor.close()
    nx.close()

    return id
