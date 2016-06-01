# basic database setup
library('RMySQL')
drv <- dbDriver('MySQL')


db <- dbConnect(drv, host='research.czxveiixjbkr.us-east-1.rds.amazonaws.com', user='user', dbname='twitterresearch', password="tw33ter12")


installer_twitter_data = dbGetQuery(db,statement="SELECT * FROM accounts")

clean_installer_twitter_data <- subset(installer_twitter_data, installer_twitter_data$num_tweets < 20000)

# number of tweets histogram and kernal density plot
hist(clean_installer_twitter_data$num_tweets, breaks=15,
	main="Distribution of number of tweets by installer",
	ylab="Frequency",
	xlab="Number of Tweets \n by Installer",
	col="grey"
	)

density <- density(clean_installer_twitter_data$num_tweets)
plot(density,
	main="Kernal Density Plot \n Number of tweets by installer",
	xlab="Tweets",
	ylab="Density",
	col="blue"
	)
polygon(density, col="blue")

# number of followers
hist(clean_installer_twitter_data$num_followers, breaks=15,
	main="Distribution of number of follower by installer",
	ylab="Frequency",
	xlab="Number of Followers \n by Installer",
	col="grey")

density2 <- density(clean_installer_twitter_data$num_followers)
plot(density2,
	main="Kernal Density Plot \n Number of Followers by installer",
	xlab="Followers",
	ylab="Density",
	col="blue"
	)
polygon(density2, col="blue")

total revenue
hist(clean_installer_twitter_data$total_revenue, breaks=15,
	main="Distribution of number of follower by installer",
	ylab="Frequency",
	xlab="Total Revenue \n by Installer",
	col="grey")

