# -*- coding: utf-8 -*-

import unittest
from classifier import *
import pymysql.cursors #https://github.com/PyMySQL/PyMySQL/


connection = pymysql.connect(host="localhost", user="root", db="twitterresearch")

class TestDatabaseTest(unittest.TestCase):
	def setUp(self):
		self.test_tweet_id = '9999999999'
		self.test_tweet = "Some radoom text"
		self.test_installer_id = '1378256179'

		query = """INSERT INTO tweets(tweet_id, tweet, twitter_id_fkey) VALUES (%s, %s, %s); """

		with connection.cursor() as cursor:
			cursor.execute(query, (self.test_tweet_id, self.test_tweet, self.test_installer_id,))
			connection.commit()


	def test_analyze_tweet(self):
		pass

	def test_assign_to_db(self):
		demo_marketing_type = '2-3'
		assign_to_database(self.test_tweet_id, demo_marketing_type )
		tweet = get_tweet(self.test_tweet_id)

		self.assertEqual(tweet[1], demo_marketing_type)

	def test_get_tweet(self):
		self.assertEqual(get_tweet(self.test_tweet_id), (self.test_tweet, None))


	def tearDown(self):
		with connection.cursor() as cursor:
			sql = "DELETE FROM tweets WHERE tweet_id = %s;" % (self.test_tweet_id,)
			cursor.execute(sql)
			connection.commit()






if __name__ == "__main__":
	unittest.main()	
			