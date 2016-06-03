import httplib
import socket
from urlparse import urlparse
import sys, os
import MySQLdb
import datetime
import time
import logging



class Database:
	# host="research.czxveiixjbkr.us-east-1.rds.amazonaws.com"
	# user="user"
	# password="tw33ter12"
	# db="twitterresearch"

	host='localhost'
	user='root'
	password='yourpassword'
	db='solar_marketing'


	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()

	def insert(self, query, object=None):
		try:
			if object is None:
				self.cursor.execute(query)

			elif isinstance(object, AnalyzedTweet):
				self.cursor.execute(query, (object.tweet_id, object.online_review, object.facebook, object.instagram))

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

class AnalyzedTweet:
	def __init__(self, tweet_id, online_review, facebook, instagram):
		self.tweet_id = tweet_id
		self.online_review = online_review
		self.facebook = facebook
		self.instagram = instagram


class Url:

	def expandUrl(self, url):
		try:
			o = urlparse(url)
			if o.scheme == 'http':
				conn = httplib.HTTPConnection(o.netloc)
			elif o.scheme == 'https':
				conn = httplib.HTTPSConnection(o.netloc)
			conn.request('HEAD', o.path)
			response = conn.getresponse()
			return response.getheader('location')

		except (httplib.HTTPException, socket.error) as ex:
   			print "Error: %s" % ex

   		except Exception as e:
   			print ("unknown error ") + e

	def parseUrl(self, url):
	
		o = urlparse(url)

		return self.__returnStrippedUrl(o.netloc.split("www."))

   	def stripUrl(self, url):
   		o = urlparse(url)
		if o.scheme == 'http':
			website = o.netloc
		elif o.scheme == 'https':
			website = o.netloc

   		return self.__returnStrippedUrl(website.split("www."))

   	def __returnStrippedUrl(self, url):

   		if(len(url) == 1):
   			return url[0]
   		else:
   			return url[1]

db = Database()

def review_blog():

	blog_urls = """SELECT DISTINCT blog FROM accounts;"""

	blog_urls_list = db.query(blog_urls)

	blog_urls_set = set()

	for i in blog_urls_list:
		url = i[0]
		blog_urls_set.add(url)

	print blog_urls_set

drop_tweet_analysis_table = """DROP TABLE IF EXISTS installer_url_analysis"""
db.insert(drop_tweet_analysis_table)

# should I see if they reference youtube.com??

create_tweet_analysis_table = """CREATE TABLE IF NOT EXISTS installer_url_analysis(
									tweet_id_fkey VARCHAR(20),
									online_review TINYINT, 
									facebook TINYINT, 
									instagram TINYINT,
									FOREIGN KEY (tweet_id_fkey) REFERENCES tweets(tweet_id));"""

db.insert(create_tweet_analysis_table)

urls_count = dict()

# #real data queried from database
# urls_used = """SELECT urls.tweet_id_fkey, urls.url_text, accounts.website, accounts.blog, accounts.company FROM urls
# 				INNER JOIN tweets on urls.tweet_id_fkey = tweets.tweet_id
# 				INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id;"""

#real data queried from database

urls_used = """SELECT urls.tweet_id_fkey, urls.url_text, accounts.company FROM urls
				INNER JOIN tweets on urls.tweet_id_fkey = tweets.tweet_id
				INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id;"""


list_urls = db.query(urls_used)


def online_review(url):
	pass


if __name__ == '__main__':
	count = 0
	obj = Url()

	for url in list_urls:
		tweet_id = url[0]
		expanded_url = obj.expandUrl(url[1])

		if expanded_url != None:
			tweeted_url = obj.parseUrl(expanded_url)
		else:
			tweeted_url = obj.parseUrl(url[1])
			expanded_url = url[1]

		# print tweeted_url

		company_url = None
		blog_url = None

		# reference_company_general = tweeted_url == company_url
		



		# # needs to be changed once the blog analysis is working working
		# if blog_url == None:
		# 	reference_company_blog = False
		# else:
		# 	reference_company_blog = blog_url in expanded_url

		online_review = tweeted_url in ['trustlink.org', 'myreviewboost.com', 'manta.com', 'yelp.com', 'angieslist.com']

		facebook = tweeted_url == 'facebook.com'
		instagram = tweeted_url == 'instagram.com'

		installer_tweet_analysis = AnalyzedTweet(tweet_id, online_review, facebook, instagram)

		query = """INSERT INTO installer_url_analysis (tweet_id_fkey, online_review, facebook, instagram)
						VALUES (%s, %s, %s, %s)"""
			
		db.insert(query, installer_tweet_analysis)
		db.connection.commit()
		count += 1

		print count
	



url_text = open('list.txt', 'w')
url_text.write('Url\tCount\n')


for url in urls_count:
	url_text.write(str(url) + '\t' + str(urls_count[url]['count']) + '\n')

url_text.close()

print 'Done.'




