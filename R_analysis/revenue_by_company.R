library('RMySQL')
drv <- dbDriver('MySQL')

db <- dbConnect(drv, host='research.czxveiixjbkr.us-east-1.rds.amazonaws.com', user='user', dbname='twitterresearch', password="tw33ter12")

installation_data = dbGetQuery(db, statement="SELECT seller_company_name, sum(total_cost) AS total_revenue_2012 FROM solar_installations WHERE YEAR(first_new_reservation_request_date) = '2012' AND current_incentive_application_status = 'Completed' GROUP BY seller_company_name")

clean_installation_data <- subset(installation_data, installation_data$total_revenue_2012 > 1000000)


hist(clean_installation_data$total_revenue_2012, breaks=100,
	main="Revenue Distribution by installers 2012 \n (limit $1 million USD)",
	ylab="Frequency",
	xlab="Millions of Dollars",
	col="blue"
	)

