import tweepy
from tweepy import Cursor
import accesskey
import sys, os
import pymysql.cursors #https://github.com/PyMySQL/PyMySQL/
import time
import accesskey

connection = pymysql.connect(host="localhost", user="root", db="twitterresearch")

def add_installer(twitter_id, installer_name):
	
	query = """INSERT INTO installers (twitter_id, installer_name)
					VALUES (%s, %s)"""	

	try:
		with connection.cursor() as cursor:
			cursor.execute(query, (twitter_id, installer_name))

		connection.commit()

	except Exception as ex:
		print(twitter_id, installer_name)
		template = "An exception of type {0} occured. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		print(message)
	


def get_rate_limit(api):
	rates = api.rate_limit_status()
	startingCalls = rates['resources']['statuses']['/statuses/user_timeline']['remaining']
	print("Number starting calls " + str(startingCalls))

def get_list(path):
	"""
	"""
	f = open('top_installer_twitter_accounts.txt', 'r')
	accounts = f.readlines()[1:]
	f.close()
	return accounts


def start_over_last_installer():
	query = """SELECT DISTINCT(`twitter_id_fkey`) FROM tweets"""
	with connection.cursor() as cursor:
		cursor.execute(query)
		result = cursor.fetchall()


	connection.commit()	
	return result


def write_tweet(connection, status):
	tweet_id = status.id
	tweet = status.text.encode('utf-8')
	
	# time and language
	tweet_date = status.created_at
	language = status.lang

	# text
	twitter_id_fkey = status.user.id
	truncated = status.truncated

	# Items related to retweeting
	retweeted = status.retweeted
	if hasattr(status, 'retweeted_status'):
		retweet = True
	else:
		retweet = False
	retweet_count = status.retweet_count

	# favoriting
	favorited = status.favorited
	favorite_count = status.favorite_count

	# geolocation
	if status.place != None:
		place = status.place
		y_coordinate = (place.bounding_box.coordinates[0][0][1] + place.bounding_box.coordinates[0][2][1]) / 2
		x_coordinate = (place.bounding_box.coordinates[0][0][0] + place.bounding_box.coordinates[0][2][0]) / 2

	elif status.coordinates != None:
		x_coordinate = status.coordinates['coordinates'][0]
		y_coordinate = status.coordinates['coordinates'][1]
	else:
		x_coordinate = None
		y_coordinate = None

	
	query = """INSERT INTO tweets (tweet_id, tweet, truncated, tweet_date, language, retweet, retweeted, retweet_count, x_coordinate, y_coordinate, favorited, favorite_count, twitter_id_fkey)
					VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"""	

	try:
		with connection.cursor() as cursor:
			cursor.execute(query, (tweet_id, tweet, truncated, tweet_date, language, retweet, retweeted, retweet_count, x_coordinate, y_coordinate, favorited, favorite_count, twitter_id_fkey))

		# connection is not autocommit by default. So you must commit to save
     	# your changes.
		connection.commit()

	except Exception as ex:
		print(tweet_id, tweet, truncated, tweet_date, language, retweet, retweeted, retweet_count, x_coordinate, y_coordinate, favorited, favorite_count, twitter_id_fkey)
		template = "An exception of type {0} occured. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		print(message)

			


def main():

	api = accesskey.getAPI(1)
	rates = api.rate_limit_status()
	current_key = 1

	account_number = 0
	count = 0

	connection = pymysql.connect(host="localhost", user="root", db="twitterresearch")

	accounts = get_list('top_installer_twitter_accounts.txt')

	for account in accounts:
		row = account.split('\t')
		twitter_id, twitter_handle, installer_name  = row[2], row[1], row[0]
		add_installer(twitter_id, installer_name)
		
		if twitter_id != "none":

			get_rate_limit(api)
			account_number += 1
			print("account "+ twitter_handle + " number " + str(account_number))
			for status in Cursor(api.user_timeline, id=twitter_id).items():
				count += 1

				if(count % 20 == 0):
					time.sleep(6)
					print("sleeping cycle: " + str(count / 20))

				write_tweet(connection, status)

	connection.close()




if __name__ == "__main__":
    main()







		



# 

# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

#     with connection.cursor() as cursor:
#     #     # Read a single record
#         sql = "SELECT 'id', `password` FROM `users` WHERE `email`=%s"
#         cursor.execute(sql, ('webmaster@python.org',))
#         result = cursor.fetchone()
#         print(result)
# finally:
#     connection.close()


