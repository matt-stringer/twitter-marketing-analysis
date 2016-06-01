import pymysql.cursors #https://github.com/PyMySQL/PyMySQL/


drop_installer_table = "DROP TABLE IF EXISTS installers"
drop_table = "DROP TABLE IF EXISTS tweets"
drop_hashtag_table = "DROP TABLE IF EXISTS hashtags"
drop_url_table = "DROP TABLE IF EXISTS urls"
drop_user_mention_table = "DROP TABLE IF EXISTS user_mentions"



create_installer_table = """CREATE TABLE IF NOT EXISTS installers(
							twitter_id BIGINT,
							installer_name VARCHAR(200),
							PRIMARY KEY (twitter_id));"""

create_table = """CREATE TABLE IF NOT EXISTS tweets(
					tweet_id BIGINT,
					tweet TEXT,
					truncated TINYINT,
					tweet_date DATETIME,
					language VARCHAR(5),
					retweet TINYINT,
					retweeted TINYINT,
					retweet_count INT,
					x_coordinate DOUBLE,
					y_coordinate DOUBLE,
					favorited TINYINT,
					favorite_count INT,
					source VARCHAR(100),
					twitter_id_fkey BIGINT NOT NULL,
					marketing_type VARCHAR(100),
					PRIMARY KEY (tweet_id),
					FOREIGN KEY (twitter_id_fkey) REFERENCES installers(twitter_id))
				ENGINE = InnoDB;"""



create_hashtag_table = """CREATE TABLE IF NOT EXISTS hashtags (
							tweet_id_fkey BIGINT,
							hashtags_text VARCHAR(60),
							FOREIGN KEY (tweet_id_fkey) REFERENCES tweets(tweet_id))
						ENGINE = InnoDB;"""



create_url_table = """CREATE TABLE IF NOT EXISTS urls(
							tweet_id_fkey BIGINT,
							url_text TEXT,
							FOREIGN KEY (tweet_id_fkey) REFERENCES tweets(tweet_id))
						
						ENGINE = InnoDB;"""



create_user_mention_table = """CREATE TABLE IF NOT EXISTS user_mentions(
								tweet_id_fkey BIGINT,
								user_mention_text TEXT,
								FOREIGN KEY (tweet_id_fkey) REFERENCES tweets(tweet_id))
								ENGINE = InnoDB;"""

def create_queries():
	query_list = [drop_hashtag_table, drop_url_table, drop_user_mention_table, drop_table, drop_installer_table, create_installer_table, create_table, create_hashtag_table, create_url_table, create_user_mention_table]

	connection = pymysql.connect(host="localhost", 
								 user="root", 
								 db="twitterresearch")

	for query in query_list:
		try:
			with connection.cursor() as cursor:
				cursor.execute(query)
			
				connection.commit()

		except Exception as e:
			print(e)

	connection.close()

			


create_queries()
