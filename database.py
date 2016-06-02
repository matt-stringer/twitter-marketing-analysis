import MySQLdb
import os

class Database:

	host='localhost'
	user='root'
	password='yourpassword'
	db='solar_marketing'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()
	def query(self, query):
		try:
			self.cursor.execute(query)
			return self.cursor.fetchall()

		except Exception as e:
			# print sys.exc_info()
			print "broken"