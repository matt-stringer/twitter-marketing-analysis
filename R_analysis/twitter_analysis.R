
# http://www.rforge.net/RJDBC/

# install.packages("RJDBC",dep=TRUE)

# USEFUL functions

#1 show names of functions
names(twitter_data)

#2 show first 5 lines of data
head(twitter_data)


# basic database setup
library('RMySQL')
drv <- dbDriver('MySQL')
db <- dbConnect(drv, host='localhost', user='root', dbname='twitterresearch', password="yourpassword")

# twitter scatterplot
twitter_data = dbGetQuery(db,statement="SELECT * FROM accounts")

twitter_data = dbGetQuery(db,statement="SELECT * FROM accounts WHERE num_followers < 5000 AND total_revenue < 2000000")

plot(twitter_data$total_revenue, twitter_data$num_followers, main="Scatterplot Revenue v. Followers", xlab="Revenue", ylab="Followers", labels=twitter_data$screen_name)
plot(twitter_data$total_installs, twitter_data$num_followers, main="Scatterplot Installs v. Followers", xlab="Installs", ylab="Followers")
plot(twitter_data$num_tweets, twitter_data$total_revenue, main="Scatterplot Revenue v. Num of Tweets", xlab="Number of Tweets", ylab="Revenue")
plot(twitter_data$total_installs, twitter_data$num_tweets, main="Scatterplot Installs v. Num of Tweets", xlab="Installs", ylab="Number of Tweets")

ggplot(twitter_data, aes(twitter_data$num_tweets, twitter_data$total_revenue)) + geom_point() + geom_text(aes(label=twitter_data$screen_name))



# all Retweets 
retweets = dbGetQuery(db,statement="SELECT screen_name, count(tweet) AS tweet_count FROM  accounts, tweets WHERE (tweets.twitter_id_fkey = accounts.twitter_id) AND retweet = 1 GROUP BY screen_name ORDER BY tweet_count")
library('ggplot2')

ggplot(data=retweets, aes(x=retweets$screen_name, y=retweets$tweet_count)) + 
geom_bar(colour="white",stat="identity") +
theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust=0.5)) + xlab("My x label") +
xlab("Screen Name") +
ylab("Number of Retweets") +
ggtitle("Number of Retweets by Installer") 



# Tweets 
tweets = dbGetQuery(db,statement="SELECT screen_name, count(tweet) AS tweet_count FROM  accounts, tweets WHERE (tweets.twitter_id_fkey = accounts.twitter_id) AND retweet = 0 GROUP BY screen_name ORDER BY tweet_count")
library('ggplot2')

ggplot(data=tweets, aes(x=tweets$screen_name, y=tweets$tweet_count)) + 
geom_bar(colour="white",stat="identity") +
theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust=0.5)) +
xlab("Screen Name") +
ylab("Number of Tweets") +
ggtitle("Number of Tweets by Installer (Not Including Retweets)") 



# not Retweets