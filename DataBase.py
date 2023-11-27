#DataBase操作
import sqlite3
import os
FILENAME = "ClientInfo.db"
TABLE_NAME = "Client"
CONNECTION = sqlite3.connect(FILENAME)
CURSOR = CONNECTION.cursor()

def execute(command:str)->int: #sql実行
	try:
		CURSOR.execute(command)
		CONNECTION.commit()
	except sqlite3.Error as e:
		print(e.args[0])
		return -1
	return CURSOR.lastrowid

def query(command:str): #クエリ実行
	CURSOR.execute(command)
	return CURSOR.fetchall()

def counter(cond:str):
	return query(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {cond};")

def print_all():
	return query(f"SELECT * FROM {TABLE_NAME}")

def close():
	CONNECTION.close()
	os.remove(FILENAME)

