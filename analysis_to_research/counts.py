import sys
import os
import cPickle as pickle
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt
from mpltools import style
from mpltools import layout
style.use(['ggplot', 'pof'])
almost_black = '#262626'
from database import Database


cwd = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(os.path.split(cwd)[0], 'data')
resultsdir = os.path.join(os.path.split(cwd)[0], 'results')

marketing = {'passive_marketing': ['environmental_impact', 'investment', 'govt_incentives', 'pv_education', 'rate_changes', 'industry_growth'],
			 'active_marketing': ['online_review', 'past_work', 'event_marketing', 'channel_partnering', 'webtools', 'promotions', 'contact', 'bragging']}


pie_colors = { 'environmental_impact': '#7C8FB0', 
			'investment': '#EEAD51', 
			'govt_incentives': '#8CC43D', 
			'pv_education': '#2B292A', 
			'rate_changes': '#FED700',
			'industry_growth': '#426986',
			'online_review': '#8B8878', 
			'past_work': '#426986', 
			'event_marketing': '#87CEFA', 
			'channel_partnering': '#EEAD51', 
			'webtools': '#8CC43D', 
			'promotions': '#2B292A', 
			'contact': '#FED700', 
			'bragging': '#D34724'}


def render_file_style(frase):
    return frase.replace("/", "").replace(" ", "").replace(".", "").replace(",", "")


db = Database()

def load_base_data():
	vectorized_file = 'pickle_files/tweets.pkl'
	if os.path.isfile(vectorized_file) == False:
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

def load_annual_count_tweets():
	vectorized_file = 'pickle_files/all_tweets.pkl'
	if os.path.isfile(vectorized_file) == False:
		tweets_query = """SELECT accounts.screen_name, accounts.company, tweets.tweet_id, tweets.tweet, tweets.tweet_date FROM tweets
							LEFT JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id;"""

		result_set = db.query(tweets_query)
		print "vectorizing file"
		serialize_object(result_set, vectorized_file)
		result_set = pickle.load(open(vectorized_file, "rb"))

	else:
		result_set = pickle.load(open(vectorized_file, "rb"))

	return result_set


def serialize_object(obj,filename):
	pkl_file = open(filename, 'wb')
	pickle.dump(obj, pkl_file)
	pkl_file.close()


def make_dataframe(query_results):
	screen_names = []
	installers = []
	tweets = []
	tweets_date = []
	classifications = []

	for i in query_results:
		screen_names.append(i[0])
		installers.append(i[1])
		tweets.append(i[3])
		tweets_date.append(i[4])
		classifications.append(i[5])
	
	d = {'screen_name': screen_names, 'installer': installers, 'tweet': tweets, 'date': tweets_date, 'classification': classifications}
	return DataFrame(data=d)

def match_year(installer, year, dictionary):
	try:
		for key, value in dictionary[installer].items():
			if str(year) == str(key):
				return value
	except KeyError as e:
		print e

def make_count_dictionary():
	tweets = load_annual_count_tweets()
	dictionary = {}

	for row in tweets:
		handle = row[0]
		company = row[1]
		year = str(row[4].year)

		if company in dictionary:
			dictionary[company]['tot_count'] += 1

			if year in dictionary[company]:
				dictionary[company][year] = dictionary[company][year] + 1
			else:
				dictionary[company][year] = 1
		else:
			dictionary[company] = {'tot_count': 1}

	return dictionary

def make_total_count_dict():
	tweets = load_annual_count_tweets()
	dictionary = {}

	for row in tweets:

		year = str(row[4].year)

		if year in dictionary:
			dictionary[year] += 1

		else:
			dictionary[year] = 1

	return dictionary






			

def main():

	results = load_base_data()
	df = make_dataframe(results)
	tweet_count_dict = make_count_dictionary()

	total_tweet_count_dict = make_total_count_dict()

	index = 0

	fig=plt.figure()
	plt.title("pie charts", fontsize=20)
	ax = plt.subplot( 111 ) 

	
	num_plots = 5

	plt.figure(figsize=(60,20), dpi=100)
	plt.title("Total", fontsize=20)

	for marketing_type in marketing:

		year_group = df.groupby(df['date'].map(lambda x: x.year))
		
		for year, group in year_group:
			

			if year < 2014:

				index += 1
				

				group = group[(group['classification'].isin(marketing[marketing_type]))]
				total_yearly_tweets = len(group)

				name_group = group.groupby(['classification']).count()

				# figure out a way to find the percentages.
				tot_count = name_group
				print tot_count

				labels = dict(name_group['classification']).keys()
				colors = []

				for label in labels:
					colors.append(pie_colors[label])

				sizes = dict(name_group['classification']).values()

				
				plt.subplot(2,num_plots,0+index)

				if index <= num_plots:
					plt.title(year, fontsize=34, fontweight='bold')

				wedges, texts = plt.pie(sizes, labels=labels, colors=colors, pctdistance=1.1, labeldistance=1.05)
				for t in texts:
					t.set_size('xx-large')
					t.set_weight('bold')
				circle=plt.Circle((0.0,0.0),.4,color='w')
				fig = plt.gcf()
				fig.gca().add_artist(circle)
				#plt.text(0.0, 0.0, "Subject ", ha='center', fontsize=13, fontweight='bold')

				for w in wedges:
   					w.set_linewidth( 2 )
    				w.set_edgecolor( 'w' )
    				w.set_alpha(0.5)

    			if index <= num_plots:
    				plt.text(-0.05, -1.4, "Social Marketing Tweets: "+ str(total_yearly_tweets), ha='center', fontsize=30, fontweight='bold')

    			elif index > num_plots:
    				plt.text(-0.05, -1.4, "Direct Marketing Tweets: "+ str(total_yearly_tweets), ha='center', fontsize=30, fontweight='bold')








	plt.savefig(resultsdir + "/marketing_pie_charts/total.png", bbox_inches='tight')


	for installer, group1 in df.groupby(['installer']):

		installer_index = 1
		fig=plt.figure()
		plt.title("pie charts", fontsize=20)

		installer_year_group = group1.groupby(group1['date'].map(lambda x: x.year))
		installer_year_group.filter(lambda x: x < 2014)

		num_plots = len(installer_year_group)
		plt.figure(figsize=(num_plots*6,8), dpi=100)
		plt.text(0.0, 0.0, "Total Tweets ", ha='center', fontsize=18, fontweight='bold')

		for marketing_type in marketing:

			tot_tweets = len(group1)
			
			for year, group2 in installer_year_group:
			
				group2 = group2[(group2['classification'].isin(marketing[marketing_type]))]
				yearly_tweets = len(group2)


				if yearly_tweets > 0: 

					colors = []

					installer_name_group = group2.groupby(['classification']).count()

					labels = dict(installer_name_group['classification']).keys()

					

					sizes = dict(installer_name_group['classification']).values()

					plt.subplot(2,num_plots,0+installer_index)
					plt.title(year)
					plt.pie(sizes, labels=labels)
					plt.text(-0.05, -1.3, "Classifed Tweets "+ str(yearly_tweets) + "\n Total Tweets " + str(match_year(installer, year, tweet_count_dict)), ha='center', fontsize=13, fontweight='bold')
					installer_index += 1

				else:
					labels = ['no tweets']
					sizes = [0]
					plt.subplot(2,num_plots,0+installer_index)
					plt.title(year)
					plt.pie(sizes, labels=labels)
					plt.text(-0.05, -1.2, "Classifed tweets 0 \n  total tweets " + str(match_year(installer, year, tweet_count_dict)), ha='center', fontsize=13, fontweight='bold')
					installer_index += 1




		# plt.savefig(resultsdir + "/marketing_pie_charts/" + render_file_style(installer) +"_" + marketing_type + ".png", bbox_inches='tight')
		plt.savefig(resultsdir + "/marketing_pie_charts/" + render_file_style(installer)  + ".png", bbox_inches='tight')


if __name__ == '__main__':
	main()	

