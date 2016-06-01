# -*- coding: utf-8 -*-

import unittest
from tweet_scraper import *

class TestDatabaseTest(unittest.TestCase):
	
	def setUp(self):
		self.test_installer_name = "ABC Installer"
		self.test_installer_id = '123412412'
		add_installer(self.test_installer_id, self.test_installer_name)
		self.connection = pymysql.connect(host="localhost", user="root", db="twitterresearch")
			

	def test_installer_written(self):
		with self.connection.cursor() as cursor:
			sql = "SELECT installer_name FROM installers WHERE twitter_id = %s"
			cursor.execute(sql, (self.test_installer_id,))
			result = cursor.fetchone()
			self.assertEqual(result[0], self.test_installer_name)

	def tearDown(self):
		with self.connection.cursor() as cursor:
			sql = "DELETE FROM installers WHERE twitter_id = %s;" % (self.test_installer_id,)
			cursor.execute(sql)
			self.connection.commit()

class ResetInstallerTest(unittest.TestCase):
	def setUp(self):
		print(start_over_last_installer())

	def test_get_last(self):
		pass
			
class TweetScraperTest(unittest.TestCase):
	def setUp(self):
		self.test_tweet = "RT @BCinnamon: @suncatchermovie @HorizonSolarPwr @SpiceSolar @ChooseEthical Thanks to Jigar and Shalini for making this event happen."

	def test_write_installer_to_db(self):
		self.assertEqual(self.test_tweet, self.test_tweet)


if __name__ == "__main__":
	unittest.main()	