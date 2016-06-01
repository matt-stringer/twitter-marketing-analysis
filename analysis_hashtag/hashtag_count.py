import httplib
import socket
from urlparse import urlparse
import sys, os
import MySQLdb
import datetime
import time
import logging


# # create a logging format
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# fh = logging.FileHandler('url_analysis.log')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# logger.addHandler(fh)

# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# ch.setFormatter(formatter)
# logger.addHandler(ch)

# logger.info('this is a test log message')

class Database:
	# host="research.czxveiixjbkr.us-east-1.rds.amazonaws.com"
	# user="user"
	# password="tw33ter12"
	# db="twitterresearch"

	host='localhost'
	user='root'
	password='yourpassword'
	db='twitterresearch'

	queryCount = 0
	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()

	def insert(self, query, object=None):
		try:
			if object is None:
				self.cursor.execute(query)

		except Exception as e:
			print sys.exc_info()
			self.connection.rollback()

	def query(self, query):
		try:
			self.cursor.execute(query)
			return self.cursor.fetchall()

		except Exception as e:
			print sys.exc_info()
			print "broken"


	def __del__(self):
		self.connection.close()

class Hashtag:
	hashtagCount = 0
	def __init__(self):
		Hashtag.hashtagCount += 1

db = Database()

hashtags_used = """SELECT hashtags.tweet_id_fkey, hashtags.hashtags_text, accounts.company, accounts.screen_name FROM hashtags
						INNER JOIN tweets on hashtags.tweet_id_fkey = tweets.tweet_id
						INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id;"""

list_hashtags = db.query(hashtags_used)

hashtag_count = dict()

if __name__ == '__main__':
	for hashtag in list_hashtags:
		obj = Hashtag()

		tweet_id = hashtag[0]
		hashtags = hashtag[1]
		company = hashtag[2]
		screen_name = hashtag[3]

		if hashtags in hashtag_count:
			hashtag_count[hashtags]['count'] += 1
		else:
			hashtag_count[hashtags] = {'count': 1}


hashtag_text = open('hashtag_list.csv', 'w')
hashtag_text.write('hashtag,Count\n')

for item in hashtag_count:
	hashtag_text.write(str(item) + ',' + str(hashtag_count[item]['count']) + '\n')

hashtag_text.close()

print "done."




