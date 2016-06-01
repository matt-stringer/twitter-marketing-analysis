import sys, os
import MySQLdb
import datetime
import codecs

cwd = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(os.path.split(cwd)[0], 'data')





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


class TaggedTweet:
	def __init__(self, tweet_id_fkey, tweet_text, tweet_date, classification, twitter_id):
		self.tweet_id_fkey = tweet_id_fkey
		self.tweet_text = tweet_text
		self.tweet_date = tweet_date
		self.classification = classification
		self.twitter_id = twitter_id

db = Database()

def make_tables():
	drop_table = "DROP TABLE IF EXISTS tweet_tags"

	create_table = """CREATE TABLE IF NOT EXISTS tweet_tags(
					tweet_id_fkey VARCHAR(30) NOT NULL,
					tweet_text TEXT,
					tweet_date DATETIME,
					classification VARCHAR(10),
					twitter_id VARCHAR(30) NOT NULL,
					FOREIGN KEY (tweet_id_fkey) REFERENCES tweets(tweet_id))
					ENGINE = InnoDB;"""

	db.insert(drop_table)
	db.insert(create_table)

def tweets_tagged(company_id):
	query = "SELECT tweet_id_fkey FROM tweet_tags WHERE twitter_id = %s"
	args = [u"{this_name}".format(this_name= company_id)]

	db.cursor.execute(query, args)
	return db.cursor.fetchall()


def company_tweets(company_id):
	query = "SELECT tweet FROM tweets WHERE twitter_id_fkey = %s" 
	args = [u"{this_name}".format(this_name= company_id)]
	db.cursor.execute(query, args)
	return db.cursor.fetchall()

def find_tagged_tweets(company_id):
	query = "SELECT tweet_id_fkey FROM tweet_tags WHERE twitter_id = %s"
	args = [u"{this_name}".format(this_name= company_id)]
	db.cursor.execute(query, args)
	return db.cursor.fetchall()

def generate_rand_tweet(company_id):
	query = "SELECT tweet_id FROM tweets WHERE twitter_id_fkey = %s ORDER BY rand() LIMIT 1;"
	args = [u"{this_name}".format(this_name= company_id)]

	db.cursor.execute(query, args)
	return db.cursor.fetchall()[0]


def populate_tables():
	f = open(datadir + "/training_set/analyzed-random-tweets.csv", "r")
	#f = codecs.open(datadir + "/training_set/analyzed-random-tweets.csv", 'r', encoding='utf-8')
	analyzed_tweets = f.readlines()[1:]
	f.close()
	error_count = 0

	for tweet in analyzed_tweets:
		try:

			row = tweet.split('?!~')
			tweet_id_fkey = row[1]

			tweet_text = row[2].encode("utf-8")
			screen_name = row[0]

			query = "SELECT twitter_id FROM accounts WHERE screen_name LIKE %s" 
			args = u"{this_name}".format(this_name= screen_name)
			db.cursor.execute(query, args)
			twitter_id = db.cursor.fetchall()[0][0]
			tweet_date = row[3]
			classification = row[4]

			tweet_tags = TaggedTweet(tweet_id_fkey, tweet_text, tweet_date, classification, twitter_id)
			query = """INSERT INTO tweet_tags(tweet_id_fkey, tweet_text, tweet_date, classification, twitter_id)
						VALUES 	(%s, %s, %s, %s, %s)"""

			db.insert(query, tweet_tags)
			db.connection.commit()

		except Exception as error:
			print error
			error_count += 1



def main():
	f1 = open('sanity_check.txt', 'w')
	f1.write("screen name" +"\t" + "Tweet ID" + "\t" + "Tweet Text" +"\t"+ "Tweet Date" + "\t" + "Type" + "\n")
	try:
		query = "SELECT twitter_id FROM tweet_tags;" 
		print len(db.query(query))
	except Exception as error:
		print error
		make_tables()
		populate_tables()


	
	else:
		companies = db.query("SELECT twitter_id, screen_name FROM accounts")
		for info in companies:
			company_id = str(info[0])
			screen_name = str(info[1])

			total_tweets = company_tweets(company_id)
			num_total_tweets = len(total_tweets)

			num_tagged_tweets = 0

			while num_tagged_tweets < (num_total_tweets * 0.2): 
				twenty_percent = (num_total_tweets * 0.2)
				print "target " + str(twenty_percent) + "  / current:  " + str(num_tagged_tweets)

				tagged_tweets = tweets_tagged(company_id)
				num_tagged_tweets = len(tagged_tweets)

				rand_tweet = generate_rand_tweet(company_id) 
				tagged_tweets = find_tagged_tweets(company_id)

				if rand_tweet not in tagged_tweets:

					query = "SELECT tweet, tweet_date FROM tweets WHERE tweet_id = %s;"
					args = [u"{this_name}".format(this_name=rand_tweet[0])]
					db.cursor.execute(query, args)
					tweet_id_fkey = str(rand_tweet[0])

					tweet_info = db.cursor.fetchall()[0]

					tweet_text = str(tweet_info[0].replace("\n", ""))


					tweet_date = tweet_info[1]


					print screen_name
					print
					print tweet_text


					label = raw_input("""------------------------ \n 
What type of tweet is this? 
0 = unrelated/spam 
1 = news/outside article/opinion on solar 
2 = company related marketing""")


					if label == "0":
						subcategory = "a"

					elif label == "1":
						subcategory = raw_input("""What type of news category is this Tweet? 
a = Reduce impact on the environment
b = Make a sound financial investment
c = Educate on incentives, policies, and elections
d = solar PV basic education
e = rate changes/Increase individual energy independence from utilities
f = growing industry
g = 
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
							



					classification = str(label + "-" + subcategory)
					twitter_id = company_id

					tweet_tags = TaggedTweet(tweet_id_fkey, tweet_text, tweet_date, classification, str(twitter_id))
					query = """INSERT INTO tweet_tags(tweet_id_fkey, tweet_text, tweet_date, classification, twitter_id)
							VALUES 	(%s, %s, %s, %s, %s)"""

					db.insert(query, tweet_tags)
					db.connection.commit()
	

					f1.write(str(tweet_id_fkey) + "?!~" + tweet_text + "?!~" + str(tweet_date.year) + "?!~"+ classification + "\n")

	f1.close()
					


					

		




	
if __name__ == '__main__':

	main()
	print "done."






