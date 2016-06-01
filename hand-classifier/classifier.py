
import pymysql.cursors #https://github.com/PyMySQL/PyMySQL/


connection = pymysql.connect(host="localhost", user="root", db="twitterresearch")

marketing = {'inbound marketing': {
				'a': 'positive environmental impact of solar', 
				'b': 'solar as an investment', 
				'c': 'solar government incentives', 
				'd': 'general education about solar', 
				'e': 'utility or buying incentive rate changes', 
				'f': 'solar as an industry is growing',
				'g': 'other',
				'h': 'electric car reference',
				'i': 'technology advancement',
				'j': 'net metering',
				'k': 'politics of solar',
				'l': 'global warming',
				'm': 'energy efficiency'},
			'outbound marketing': {
			 	'a':'showcasing a customer review of the company (ie yelp)', 
			 	'b':'picture or description of past work', 
			 	'c':'promoting an event or a trade show the company will be at', 
			 	'd':'highlighting a partnership with or acquision of another company (ie hardware store or another installer)', 
			 	'e':'Informing buyers about their referrals', 
			 	'f':'Information regarding promotion or rebate', 
			 	'g':'to update to customer service',
			 	'h':'other',
			 	'i': 'link to blog',
			 	'j': 'new apps or webtools'},
			 'spam or unrelated': {
			 	'a': 'spamola'
			 },
			 'Customer Service': {
			 	'a': 'cs'
			 },
			 'jobs or hires': {
			 	'a': 'jp'
			 }}

def get_list(path):
	"""
	"""
	f = open(path, 'r')
	accounts = f.readlines()
	f.close()
	return accounts

def get_tweet(tweet_id):
	"""
	Return the tweet name and the marketing type for analysis

	args: tweet_id

	return: the tweet and the marketing for analysis

	"""

	query = """SELECT tweet, marketing_type FROM tweets WHERE tweet_id = %s; """

	with connection.cursor() as cursor:
		cursor.execute(query, (tweet_id,))
		return cursor.fetchone()


def analyze_tweet(tweet):
	"""
	Review tweet and give analysis

	args: tweet

	return: the type of marketing
	"""
	
	print('\n' + ("*"*100) + '\n')
	print(tweet + '\n')
	high_level = input("Select the the type of marketing\n 1) inbound\n 2) outbound\n 3) Spam or Unrelated\n 4) Customer Service\n 5) Jobs or Hires\n\n")
	high_level_types = {'1': 'inbound marketing', '2': 'outbound marketing', '3': 'spam or unrelated' }
	print('Select Corresponding Type of Marketing')

	if high_level in ['3', '4', '5']:
		specific = 'a'

	else:

		if high_level in high_level_types:
			trigger = high_level_types[high_level]

			for index, types in sorted(marketing[trigger].items()):
				print(" " + index + ") " + types)

			specific = input("\nEnter the corresponding letter\n")

	market_type = high_level + "-" + specific

	return market_type

def assign_to_database(tweet_id, marketing_type):
	"""
	Take the tweet and assign it to the database
	"""
	query = """UPDATE tweets SET marketing_type=%s WHERE tweet_id=%s;"""

	with connection.cursor() as cursor:
		cursor.execute(query, (marketing_type, tweet_id, ))
		connection.commit()

def write_to_file(market_type):
	pass


def main():

	random_tweets = get_list('tweets_to_analyze.txt')

	for tweet_data in random_tweets:
		tweet_id = tweet_data.split('\t')[0]

		tweet = get_tweet(tweet_id)

		market_type = analyze_tweet(tweet[0])
		assign_to_database(tweet_id, market_type)







if __name__ == '__main__':
	main()