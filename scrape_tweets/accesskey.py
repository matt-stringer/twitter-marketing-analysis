import tweepy

def getAPI(index):
	if(index == 1):

		consumer_key = "mCEkGY2Y5Rxxh77EbZdjzw"
		consumer_secret = "lgf5ai8L1cDTfesb5HVzfbQBdIvvQIFKL7bshgRDF5A"
		token = "605050044-aMeaDE0PlN8FYgMc6om1ILlwlLcn1IxSvopiOjaw"
		token_secret = "JlNIk0f5roJCmWLwAFZs5S1RR5weAhf6pdZTZxDp7I"
	else:

		consumer_key = "OZPwTm3WYS7CVedzEORBCA"
		consumer_secret = "PGY3fb0L0riLwyza7ijaXxmj65aQiJUeMRQmYjZbo8"
		token = "1923665220-PwlHRaPxruUphnUSys6GjNmDPurrmXPmPWihu3i"
		token_secret = "5o4q7KiDPerOVEfqcNTr4V5wuhyEsa39Mm7iBc8Aw"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(token, token_secret)
	api = tweepy.API(auth)
	return api

	try:
	    redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
	    print('Error! Failed to get request token.')

	print('Access key load')
