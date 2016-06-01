from database import Database
import os
import cPickle as pickle
from nltk import metrics, stem, tokenize


db = Database()

def normalize_tweet(s):
	words = tokenize.wordpunct_tokenize(s.lower().strip())
	return ' '.join([w for w in words])

def serialize_object(obj,filename):
	pkl_file = open(filename, 'wb')
	pickle.dump(obj, pkl_file)
	pkl_file.close()


def load_base_data():
	vectorized_file = 'tweets_rebates.pkl'
	if os.path.isfile(vectorized_file) == False:
		# tweets_query = """SELECT accounts.screen_name, accounts.company, tweets.tweet_id, tweets.tweet, tweets.tweet_date, tweet_classifications.classification FROM tweet_classifications 
		# 				INNER JOIN tweets on tweets.tweet_id = tweet_classifications.tweet_id_fkey 
		# 				INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id
		# 				WHERE tweet_classifications.classification = 'promotions';"""

		tweets_query = """SELECT accounts.screen_name, accounts.company, tweets.tweet_id, tweets.tweet, tweets.tweet_date, tweet_classifications.classification FROM tweet_classifications 
				INNER JOIN tweets on tweets.tweet_id = tweet_classifications.tweet_id_fkey 
				INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id;"""



		result_set = db.query(tweets_query)
		print "vectorizing file"
		serialize_object(result_set, vectorized_file)
		result_set = pickle.load(open(vectorized_file, "rb"))

	else:
		result_set = pickle.load(open(vectorized_file, "rb"))

	return result_set


def main():
	tweets =  load_base_data()
	stuff = []
	for row in tweets:
		
		tweet = row[3]
		if "rebate" or "referral"  in normalize_tweet(tweet):
			#or "referral" or "rebate"

			print row[1], row[4].month, row[4].year, tweet

			dollar_amount = [word for word in tweet.split() if word.startswith('$')]

			if dollar_amount != []:
				print dollar_amount

			if row[1] not in stuff:
				stuff.append(row[1])

				

	print len(stuff)

if __name__ == '__main__':
	main()	

