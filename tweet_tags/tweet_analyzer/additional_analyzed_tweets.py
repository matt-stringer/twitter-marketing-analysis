import sys
import MySQLdb
import cPickle as pickle
import os
import datetime
import codecs

class Database:
	# host="research.czxveiixjbkr.us-east-1.rds.amazonaws.com"
	# user="user"
	# password="tw33ter12"
	# db="twitterresearch"

	host="localhost"
	user="root"
	password="yourpassword"
	db="twitterresearch"

	queryCount = 0

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8', use_unicode=True)
		self.cursor = self.connection.cursor()

	def query(self, query):
		try:
			self.cursor.execute(query)
			return self.cursor.fetchall()



		except Exception as e:
			print sys.exc_info()
			self.connection.rollback()


	def __del__(self):
		self.connection.close()

def label_me(tweet,f):

	screen_name = tweet[0].encode('utf-8', 'ignore')
	tweet_id = tweet[1].encode('utf-8', 'ignore')
	tweet_text = tweet[2].encode('utf-8', 'ignore')
	tweet_date = tweet[3].encode('utf-8', 'ignore')

	print "The tweet is:"  ,tweet_text

	while True:
		label = raw_input("""------------------------ \n 
What type of tweet is this? 
0 = unrelated/spam 
1 = news/outside article/opinion on solar 
2 = company related marketing 
- "exit" to end:  """)
		if label == "0" or label == "1" or label == "2" or label == 'exit':
			break
		else:

			print "wrong option provided, try again"
			print "-----------------------"
			print screen_name, tweet_text

	if label == "0":
		subcategory = "a"

	elif label == "1":
		subcategory = raw_input("""What type of news category is this Tweet? 
a = company blog post
b = solar related news
c = opinions (no websites in Tweet)
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

	f.write( screen_name + "?!~" + tweet_id  + "?!~" + tweet_text + "?!~"+str(tweet_date.strftime("%Y-%m-%d"))+ "?!~"  + str(label) + "-" + subcategory + "\n")


def serialize_object(object_,filename):
	file_pickle = open(filename, "wb")
	pickle.dump(object_, file_pickle)
	file_pickle.close()


def main():
	file_all_tweets = "tweet_list_pickle.pkl"
	tweet_list = None

	if os.path.isfile(file_all_tweets) == False:
		db = Database()
		tweets_query = """SELECT accounts.screen_name, tweets.tweet_id, tweets.tweet, tweets.tweet_date FROM tweets
						INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id""" 


		tweets = db.query(tweets_query)

		tweet_list = [tweet for tweet in tweets]
		serialize_object(tweet_list,file_all_tweets)
		
	else:
		tweet_list = pickle.load(open(file_all_tweets, "rb"))
		print len(tweet_list)
		labelled_tweets = set()

		labelled_tweets_file = "/Users/mattstringer/research/twitter-research/Data/analyzed-random-tweets.txt"
		f = codecs.open(labelled_tweets_file,'r+', encoding='utf-8')
		

		for i in f.readlines()[1:]:
			row = i.split('?!~')
			labelled_tweets.add(row[1])


		while len(tweet_list) > 0:
			c = raw_input("Do u want to continue ?? y or n")
			if(c == 'n'):
				print 'Good bye'
				serialize_object(tweet_list,file_all_tweets)
				f.close()
				sys.exit(0)

			tweet = tweet_list.pop()
			if(tweet[1] not in labelled_tweets):
				label_me(tweet,f)








if __name__ == '__main__':
	main()
