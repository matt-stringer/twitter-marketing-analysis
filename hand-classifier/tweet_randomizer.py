import pymysql.cursors #https://github.com/PyMySQL/PyMySQL/
import random

connection = pymysql.connect(host="localhost", user="root", db="twitterresearch")

def load_data():
	"""
	Get for each installer the number of tweets tweeted and 
	the number of marked with marketing type

	return 
	--
	as a list of tuples for each one
	"""

	query = """SELECT twitter_id_fkey, 
					count(*) as Total,
					sum(case when marketing_type IS NOT NULL then 1 else 0 end) TweetsWithMarketType
					FROM tweets 
					GROUP BY twitter_id_fkey"""

	with connection.cursor() as cursor:
		cursor.execute(query)
		result = cursor.fetchall()

	return result

def random_tweets(installer, tweets_to_get):
	"""
	Get 20 percent of the tweets randomly for each installer set 

	in
	-- 
	installer_id, total number of tweets

	return 
	--
	set of 20 percent of tweets
	"""
	query = """SELECT tweet_id, tweet FROM tweets 
				WHERE twitter_id_fkey = %s
				ORDER BY RAND()
				LIMIT %s"""

	with connection.cursor() as cursor:
		cursor.execute(query, (installer, tweets_to_get))
		result = cursor.fetchall()

	return result


def randomize_tweets(tweets):
	"""
	Group all tweets into one set and randomize the set
	"""
	
	random.shuffle(tweets,random.random)
	return tweets
	
def write_file(tweets_list):
	f = open('tweets_to_analyze.txt', 'w')

	for tweet in tweets_list:

		f.write(str(tweet[0]) + "\t" + str(tweet[1].encode('utf-8')) + "\n")

	f.close()


def main():
	"""
	Ana

	"""
	installers = load_data()

	tweets_list = []
	

	for installer in installers:
		installer_id = installer[0]
		tweets_to_get = round(installer[1] * .20)
		tweets_list += random_tweets(installer_id, tweets_to_get)

	randomized_tweets_list = randomize_tweets(tweets_list)
	write_file(randomized_tweets_list)

	





		

if __name__ == "__main__":
    main()




