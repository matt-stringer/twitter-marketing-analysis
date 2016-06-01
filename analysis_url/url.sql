-- Select distinct 

SELECT accounts.company, accounts.website, sum(installer_tweet_analysis.reference_company_general) AS num_references FROM installer_tweet_analysis
	INNER JOIN tweets ON tweets.tweet_id = installer_tweet_analysis.tweet_id_fkey
	INNER JOIN accounts ON tweets.twitter_id_fkey = accounts.twitter_id
	WHERE installer_tweet_analysis.reference_company_general = 1
	GROUP BY accounts.company
	ORDER BY num_references DESC;


-- Number of Blog post references

SELECT accounts.company, accounts.blog, sum(installer_tweet_analysis.reference_company_blog) AS num_references FROM installer_tweet_analysis
	INNER JOIN tweets ON tweets.tweet_id = installer_tweet_analysis.tweet_id_fkey
	INNER JOIN accounts ON tweets.twitter_id_fkey = accounts.twitter_id
	WHERE installer_tweet_analysis.reference_company_blog = 1
	GROUP BY accounts.company
	ORDER BY num_references DESC;


	
