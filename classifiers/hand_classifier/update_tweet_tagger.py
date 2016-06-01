import sys, os
import MySQLdb
import datetime
import codecs






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
    	self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8', use_unicode=True)
    	self.cursor = self.connection.cursor()

    def insert(self, query, object=None):
    	try:
    		if object is None:
    			self.cursor.execute(query)
    		elif isinstance(object, TaggedTweet):
    			self.cursor.execute(query, (object.tweet_id_fkey, object.tweet_text, object.tweet_date, object.classification, object.twitter_id))


    	except Exception as e:
    		print sys.exc_info()
    		self.connection.rollback()

    def query(self, query):
		try:
			self.cursor.execute(query)
			return self.cursor.fetchall()

		except Exception as e:
			print sys.exc_info()
			self.connection.rollback()
			print "exception"	


db = Database()





	label = raw_input("""------------------------ \n 
What type of tweet is this? 
0 = unrelated/spam 
1 = news/outside article/opinion on solar 
2 = company related marketing""")


					if label == "0":
						subcategory = "a"

					elif label == "1":
						subcategory = raw_input("""What type of news category is this Tweet? 
a = Promoting or explaining electric cars
b = Make a sound financial investment
c = Educate on incentives, policies, and elections
d = solar PV basic education
e = rate changes/Increase individual energy independence from utilities
f = growing industry
g = nothing
h = undetermined
""")

# reduce a barrier
# build confidence
## everyone is d1oing it		

					elif label == "2":
						subcategory = raw_input("""What type of marketing category is this Tweet
a = link to online review
b = showcase past work
c = event marketing
d = channel marketing example
e = webtool promotion (online survey, payback caluculator)
f = promotion of incentive
g = direct company contact channel
h = proving they are the best
""")