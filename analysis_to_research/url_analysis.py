import httplib
import socket
from urlparse import urlparse
import sys, os
import MySQLdb
import datetime
import time
import logging


# create a logging format
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('url_analysis.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('this is a test log message')



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

			elif isinstance(object, AnalyzedTweet):
				self.cursor.execute(query, (object.tweet_id, object.reference_company_general, object.reference_company_blog, object.reference_company_facebook, object.reference_company_instragram))

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

	def list(self, query):
		try:
			self.cursor.execute(query)
			return self.cursor.fetchall()

		except Exception as e:
			print sys.exc_info()
			print "broken"
			

	def __del__(self):
		self.connection.close()

class AnalyzedTweet:
	def __init__(self, tweet_id, reference_company_general, reference_company_blog, reference_company_facebook, reference_company_instragram):
		self.tweet_id = tweet_id
		self.reference_company_general = reference_company_general
		self.reference_company_blog = reference_company_blog
		self.reference_company_facebook = reference_company_facebook
		self.reference_company_instragram = reference_company_instragram

class Url:
	urlCount = 0
	

	def __init__(self, blogUrlsSet):
		Url.urlCount += 1
		self.blogUrlsSet = blogUrlsSet

	def displayCount(self):
		print "Total urls counted is %d" % Url.urlCount

	def socialMediaUrl(self, url):
		return url in self.blogUrlsSet

	def expandUrl(self, url):
		try:
			o = urlparse(url)
			if o.scheme == 'http':
				conn = httplib.HTTPConnection(o.netloc)
			elif o.scheme == 'https':
				conn = httplib.HTTPSConnection(o.netloc)

			conn.request('HEAD', o.path)

			response = conn.getresponse()
			logger.info(" website " + o.netloc +" -- sever status: " + str(response.status) + " reason: " + response.reason)

			return response.getheader('location')

		except (httplib.HTTPException, socket.error) as ex:
   			print "Error: %s" % ex
   			logger.error("Failed to write %s" % ex, exc_info=True)

   		except KeyboardInterrupt as k1:
   			raise k1

   		except:
   			print ("unknown error")

	
   		

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

blog_urls = """SELECT DISTINCT blog FROM accounts;"""

blog_urls_list = db.query(blog_urls)

blog_urls_set = set()

for i in blog_urls_list:
	url = i[0]
	blog_urls_set.add(url)

print blog_urls_set

drop_tweet_analysis_table = """DROP TABLE IF EXISTS installer_tweet_analysis"""
db.insert(drop_tweet_analysis_table)

# show I see if they reference youtube.com??

create_tweet_analysis_table = """CREATE TABLE IF NOT EXISTS installer_tweet_analysis(
									tweet_id_fkey VARCHAR(20),
									reference_company_general TINYINT,
									reference_company_blog TINYINT,
									reference_company_facebook TINYINT,
									reference_company_instragram TINYINT,
									FOREIGN KEY (tweet_id_fkey) REFERENCES tweets(tweet_id));"""

db.insert(create_tweet_analysis_table)

urls_count = dict()

#real data queried from database
urls_used = """SELECT urls.tweet_id_fkey, urls.url_text, accounts.website, accounts.blog, accounts.company FROM urls
				INNER JOIN tweets on urls.tweet_id_fkey = tweets.tweet_id
				INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id;"""

list_urls = db.query(urls_used)

#test data, testing garbage website url, real url and one that timeouts 
# list_urls = [[1, "asdfasdfa"], 
# [3, "www.google.com"], 
# [7, "asdfasdfasdf"], 
# [5, "https://mail.python.org/pipermail/python-dev/2010-July/101266.html"]]



if __name__ == '__main__':

	obj = Url(blog_urls_set)

	for url in list_urls:
		tweet_id = url[0]
		expanded_url = obj.expandUrl(url[1])

		if expanded_url != None:
			tweeted_url = obj.parseUrl(expanded_url)
		else:
			tweeted_url = obj.parseUrl(url[1])
			expanded_url = url[1]

		company_url = obj.stripUrl(url[2])



		blog_url = url[3]

		reference_company_general = tweeted_url == company_url
		


		# needs to be changed once the blog analysis is working working
		if blog_url == None:
			reference_company_blog = False
		else:
			reference_company_blog = blog_url in expanded_url

		reference_company_facebook = tweeted_url == 'facebook.com'
		reference_company_instragram = tweeted_url == 'instagram.com'

		installer_tweet_analysis = AnalyzedTweet(tweet_id, reference_company_general, reference_company_blog, reference_company_facebook, reference_company_instragram)

		query = """INSERT INTO installer_tweet_analysis (tweet_id_fkey, reference_company_general, reference_company_blog, reference_company_facebook, reference_company_instragram)
						VALUES (%s, %s, %s, %s, %s)"""
			
		db.insert(query, installer_tweet_analysis)
		db.connection.commit()
	

		if tweeted_url in urls_count:
			urls_count[tweeted_url]['count'] += 1
		else:
			urls_count[tweeted_url] = {'count': 1}

url_text = open('list.txt', 'w')
url_text.write('Url\tCount\n')


for url in urls_count:
	url_text.write(str(url) + '\t' + str(urls_count[url]['count']) + '\n')

url_text.close()

print 'Done.'




