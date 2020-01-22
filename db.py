import sqlite3

from singleton import Singleton

class DB(metaclass=Singleton):
	__instance = None
	conn = None

	def __init__(self, dbpath = ""):
		try:
			self.conn = sqlite3.connect(dbpath)
		except sqlite3.OperationalError as e:
			print(f"We were unable to connect to db: {dbpath}")

	def store_xss(self, url, param):
		try:
			if self.conn is not None:
				self.conn.execute("INSERT INTO xss VALUES (?, ?)", (url, param))
				self.conn.commit()
		except sqlite3.OperationalError as e:
			print(f"We where unable to store the found XSS in the DB: {e}")
		except sqlite3.IntegrityError as e:
			pass

