# -*- coding: utf-8 -*-
import MySQLdb
import sys
import os
import CMUTweetTagger
import scipy
from sklearn.feature_extraction.text import CountVectorizer
import cPickle as pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import codecs
from sklearn.metrics import confusion_matrix
import pylab as pl
from sklearn import svm, cross_validation
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from ensemble import *
import getopt
from smote import SMOTE
import re
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk.stem


cwd = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(os.path.split(cwd)[0], 'data')
resultsdir = os.path.join(os.path.split(cwd)[0], 'results')


""""
Some good examples here

https://github.com/darkrho/yatiri/blob/master/scripts/categories_clustering.py

"""

tweet_stack_command = "java -XX:ParallelGCThreads=2 -Xmx500m -jar /Users/mattstringer/research/twitter-research/tweet_tags/ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar"
url_regex = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

english_stemmer = nltk.stem.SnowballStemmer('english')

class StemmedCountVectorizer(CountVectorizer):
	def build_analyzer(self):
		analyzer = super(StemmedCountVectorizer, self).build_analyzer()

		return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

class StemmedTfidfVectorizer(TfidfVectorizer):
	"""
	Tokenizes text, throw away words that occur too often, 
	throw away words that occur too seldom, count words that remain,
	calculate values from the counts
	"""

	def build_analyzer(self):
		analyzer = super(TfidfVectorizer, 
			self).build_analyzer()
		return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


class ClassifyTweet:
	def __init__(self, tweet_id_fkey, classification):
		self.tweet_id_fkey = tweet_id_fkey
		self.classification = classification


class Database:
	# host="research.czxveiixjbkr.us-east-1.rds.amazonaws.com"
	# user="user"
	# password="tw33ter12"
	# db="twitterresearch"

	host='localhost'
	user='root'
	password='yourpassword'
	db='solar_marketing'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()


	def insert(self, query, object=None):
		try:
			if object is None:
				self.cursor.execute(query)
			elif isinstance(object, ClassifyTweet):
				self.cursor.execute(query, (object.tweet_id_fkey, object.classification))
		
		except Exception as e:
			print sys.exc_info()
			self.connection.rollback()
			print "exception"


	def query(self, query):
		try:
			self.cursor.execute(query)
			return self.cursor.fetchall()

		except Exception as e:
			# print sys.exc_info()
			print "broken"


db = Database()


drop_table = "DROP TABLE IF EXISTS tweet_classifications;"
db.insert(drop_table)


create_table = """CREATE TABLE IF NOT EXISTS tweet_classifications(
					tweet_id_fkey BIGINT,
					classification VARCHAR(50))"""

db.insert(create_table)


# def clear_prior_matches():
# 	clear_data = """UPDATE addresses SET col_app_num_original_fkey = NULL;""" 
# 	db.insert(clear_data)
# 	db.connection.commit()


# def write_to_db(install_app_num, ad_id_num):
# 	update_query1 = """UPDATE addresses SET col_app_num_original_fkey = %s WHERE RP1PRCLID = %s"""
# 	update_items1 = UpdateItems(install_app_num, ad_id_num)

# 	#print ad_street_name, ad_house_num, ad_unit_num, install_street_name, install_unit_num, install_house_num
# 	db.insert(update_query1, update_items1)
# 	db.connection.commit()

def remove_url():
	pass


def serialize_object(obj,filename):
	pkl_file = open(filename, 'wb')
	pickle.dump(obj, pkl_file)
	pkl_file.close()

def pos_tag_tweets(tweet_list,pkl_file = 'pickle/pos_tweets.pkl'):
	
	tagged_tweets = CMUTweetTagger.runtagger_parse(tweet_list, run_tagger_cmd=tweet_stack_command)

	if pkl_file != None:
		serialize_object(tagged_tweets,pkl_file)

	return tagged_tweets


def unlabeled_corpus_maker(filename,labeled_tweet_ids,transformer):

	corpus = []
	tweet_list = None

	if os.path.isfile(filename) == False:
		
		tweets_query = """SELECT accounts.screen_name, tweets.tweet_id, tweets.tweet, tweets.tweet_date FROM tweets
						INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id""" 
		result_set = db.query(tweets_query)



		print ' db query sucessful'

		tweet_list = [tweet for tweet in result_set]

		unlabeled_tweets = []
		miss_count = 0
		unlabeled_tweet_ids =[]

		for tweet in tweet_list:
			twitter_handle = tweet[0]
			tweet_id  = tweet[1]

			if tweet_id not in labeled_tweet_ids:
				try:
					tweet_text = tweet[2].decode('utf-8', 'ignore')
					tweet_text = re.sub(url_regex, ' ', tweet_text)

				except UnicodeEncodeError as e:
					miss_count += 1
					print e
					continue

				unlabeled_tweets.append(tweet_text)
				unlabeled_tweet_ids.append(tweet_id)


		assert len(unlabeled_tweets) == len(unlabeled_tweet_ids)

		# print type(tagged_tweets)
		# # for i in tagged_tweets:
		# # 	if len(i) == 1:
		# # 		print i

		# print len(unlabeled_tweet_ids)
		# print len(tagged_tweets)
		# assert len(tagged_tweets) == len(unlabeled_tweet_ids)


		# count = 0

		# for tagged_tweet in tagged_tweets:
		# 	temp_list = [] # filtered words of a tweet
		# 	for word in tagged_tweet:
		# 		if word[1] != "U":
		# 			temp_list.append(word[0])

		# 	filtered_tweet = ' '.join(temp_list)
		# 	corpus.append(filtered_tweet)
		# 	count += 1


		vector_tweets = transformer.transform(unlabeled_tweets)

		assert len(unlabeled_tweet_ids) == vector_tweets.shape[0]

		print 'vectorize sucessful'

		serialize_object(vector_tweets, filename)
		serialize_object(unlabeled_tweet_ids,'pickle/tweet_ids.pkl')

	return vector_tweets

def get_postive_negative(class_code):
	pass


def corpus_maker(tweets,positive_classification_type,corpus_filename ,negative_classification_type=""):
	

	y = []
	corpus = []


	corpus_dict = {}
	count = 0
	miss_count=0
	neg_count =0

	labeled_tweet_ids = set()

	vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english', charset_error='ignore')

	tweets_list=[]


	for row in tweets:
		# try:
		# 	row = i.decode('utf-8', 'ignore').split('?!~')
		# except UnicodeEncodeError as e:
		# 	miss_count += 1
		# 	continue

		if(len(row) == 5):
			tweet_id = row[1]
			tweet_text = row[2].strip().replace("\n","")
			classification = row[4].strip()
			if classification == positive_classification_type:
				label = 1
				tweets_list.append(tweet_text)
				y.append(label)

			# this is where the problem is 
			elif classification != positive_classification_type:
				# print classification
				label = -1
				tweets_list.append(tweet_text)
				y.append(label)
				neg_count += 1

			labeled_tweet_ids.add(tweet_id)

	tagged_tweets = CMUTweetTagger.runtagger_parse(tweets_list, run_tagger_cmd=tweet_stack_command)

	print "len tagged tweets " + str(len(tweets_list))
	print "len tagged tweets " + str(len(tagged_tweets))

	for tagged_tweet in tagged_tweets:
		temp_list = [] # filtered words of a tweet
		for word in tagged_tweet:
			if word[1] != "U":
				temp_list.append(word[0].lower())

		filtered_tweet = ' '.join(temp_list)
		corpus.append(filtered_tweet)
		corpus_dict[filtered_tweet] = tweet_id
		
		count += 1

	vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english', charset_error='ignore')



	counts = vectorizer.fit_transform(corpus) # rename counts to tfiidf_counts

	print vectorizer.get_feature_names()

	#transformer = TfidfTransformer()
	x = counts #transformer.fit_transform(counts)
	serialize_object( (y,x,vectorizer,labeled_tweet_ids), corpus_filename)

	return (y,x,vectorizer,labeled_tweet_ids)


def evaluate_classifier(clf,test_x,test_y,train_x,train_y):
	
	pred_y = clf.predict(test_x)	
	prec_recall = precision_recall_fscore_support(test_y, pred_y)
	cm = confusion_matrix(test_y, pred_y)

	cnt_minus_one =0
	cnt_plus_one = 0
	# use this as a reference: http://en.wikipedia.org/wiki/Precision_and_recall	
	for i in test_y:
		if i == -1:
			cnt_minus_one += 1
		else:
			cnt_plus_one += 1


	print ' The -1 class entries in test set' , cnt_minus_one
	print ' The 1 class entries in test set', cnt_plus_one

	cnt_plus_one =0
	cnt_minus_one =0

	for i in train_y:
		if i == -1:
			cnt_minus_one += 1
		else:
			cnt_plus_one += 1

	print ' The -1 class entries in train set', cnt_minus_one 
	print ' The 1 class entries in train set', cnt_plus_one
	
	print 
	print cm
	
	print
	print cm[0][0], "0 class labelled as 0"
	print cm[0][1], "0 class labelled as 1"
	print cm[1][0], "1 class labelled as 0"
	print cm[1][1], "1 class labelled as 1"

	print 'precision recall'
	print 
	print prec_recall

	pl.matshow(cm)
	pl.title('Confusion matrix')
	pl.colorbar()
	pl.ylabel('True label')
	pl.xlabel('Predicted label')
	#pl.show()

def cross_validate(clf,x,y):
	scores_f1 = cross_validation.cross_val_score(clf, x, y, cv=5,scoring='f1')
	scores_prec = cross_validation.cross_val_score(clf, x, y, cv=5,scoring='precision')
	scores_recall = cross_validation.cross_val_score(clf, x, y, cv=5,scoring='recall')
	
	avg_f1 = 1.0*sum(scores_f1)/len(scores_f1)
	avg_prec = 1.0*sum(scores_prec)/len(scores_prec)
	avg_recall = 1.0*sum(scores_recall )/len(scores_recall)

	results=[avg_f1,avg_prec,avg_recall]
	return results

def myrange(start,stop,step):
	x=[]
	while(start < stop):
		x.append(start)
		start += step

	return x

# lserach for best F1. This may not be the case always.

def line_search(clf, x,y):
	max_f1 = 0
	max_c = 0

	for i in myrange(0.1,1,0.1):
		clf = clf.set_params(C = i)
		# print 'classifier with C = ', i
		results = cross_validate(clf,x,y)
		if(results[0] > max_f1):
			max_f1 = results[0]
			max_c = i


	return (max_f1,max_c,)


def count_classes(y):
	count_positive = 0
	count_negative = 0
	for i in y:
		if i == 1:
			count_positive += 1
		else:
			count_negative += 1

	return count_positive, count_negative


def oversample(train_x, train_y):

	#Use smote to balance the datasets
	count_positive, count_negative = count_classes(train_y)

	print ' The -1 class entries in test set' , count_negative
	print ' The 1 class entries in test set', count_positive

	
	ratio = round(count_negative/count_positive)

	minority_samples = np.empty([count_positive,train_x.shape[1]])
	majority_samples = np.empty([count_negative, train_x.shape[1]])

	minority_index = 0
	majority_index = 0

	assert(train_x.shape[0] == len(train_y))


	for i in range(train_x.shape[0]):
		if train_y[i] == 1:
			minority_samples[minority_index] = train_x[i].todense()
			minority_index += 1
		elif train_y[i] == -1:
			majority_samples[majority_index] = train_x[i].todense()
			majority_index += 1

	s = SMOTE(minority_samples, int(ratio*100), 5)

	print minority_samples.shape
	print majority_samples.shape

	y_minority = [1]*s.shape[0]
	y_majority = [-1]*count_negative

	y_synthetic = y_minority + y_majority

	x_synthetic = np.vstack((s,majority_samples))

	return x_synthetic, y_synthetic

def return_matches(tweet_id):

	db = Database()

	query = """SELECT accounts.screen_name, accounts.company, tweets.tweet, tweets.tweet_date FROM tweets
				INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id 
				WHERE tweets.tweet_id = %s"""

	args = u"{this_name}".format(this_name= tweet_id)

	db.cursor.execute(query, args)
	query_results = db.cursor.fetchall()
	return query_results

def my_cross_validation(clf, x, y, n):
	skf = cross_validation.StratifiedKFold(y, n)

	for train_index, test_index in skf:
		train_x, test_x = x[train_index], x[test_index]
		train_y, test_y = y[train_index], y[test_index]

		print train_x.shape[0], test_x.shape[0]

		clf_boost = AdaBoost((train_x,train_y), 2)
		clf_boost.make_strong_learner(clf)
		pred_test = clf_boost.predict(test_x)
		evaluate_classifier(clf_boost,test_x,test_y,train_x,train_y)
		clf_ensemble = Ensemble1((train_x,train_y))
		clf_ensemble.set_rule(clf);
		pred_test = clf_ensemble.predict(test_x)
		evaluate_classifier(clf_ensemble,test_x,test_y,train_x,train_y)

def write_to_file(results, classification):
	f = open(resultsdir + '/' + classification + '.csv', 'w')
	for i in results:
		twittter_handle = i[0]
		company = i[1]
		tweet = i[2]
		date_tweeted = i[3]

		f.write(twittter_handle + "," + company + ","+ tweet + "," + date_tweeted.strftime('%m/%d/%Y') + '\n')
	f.close()


def main(class_name, code):
	# class_name = ''
	corpus_filename = ''
	unlabeled_vectorized_file = 'pickle/unlabeled_vector.pkl'

  	corpus_filename = 'pickle/corpus_' + class_name + '.pkl'

	x = None
	vectorizer = None
	labeled_tweet_ids = None

	cwd = os.path.dirname(os.path.abspath(__file__))
  	directory = os.path.join(os.path.split(cwd)[0])
   	# training_set = datadir + '/tagged_tweets.txt'

   	query  = """SELECT tweets.tweet_id, tweets.tweet_id, tweets.tweet, tweets.tweet_date, tweet_tags.classification FROM tweet_tags 
   					LEFT JOIN tweets ON tweets.tweet_id = tweet_tags.tweet_id_fkey;"""

	training_set = db.query(query)


	if os.path.isfile(corpus_filename) == False:
		code = class_code[class_name]
		(y,x,vectorizer,labeled_tweet_ids) = corpus_maker(training_set, code,corpus_filename)
		print x.shape, len(y)
	else:
		print "loading from pickle file"
		(y,x,vectorizer,labeled_tweet_ids) = pickle.load(open(corpus_filename, "rb"))

		# this should be combined
		for num, tweet_id in enumerate(labeled_tweet_ids):
			print num, return_matches(tweet_id)

	unlabeled_vectors = None

	if os.path.isfile(unlabeled_vectorized_file) == False:
		unlabeled_vectors = unlabeled_corpus_maker(unlabeled_vectorized_file, labeled_tweet_ids ,vectorizer)
	else:
		unlabeled_vectors = pickle.load(open(unlabeled_vectorized_file,"rb"))

	print "Unlabled shape"	
	print unlabeled_vectors.shape

	# THE ACTUAL SYSTEM WITHOUT ANY VALIDATION
	train_x = x
	train_y = y

	if False:
		print ' i did not run'
		train_x,test_x,train_y,test_y= cross_validation.train_test_split(x,y,test_size = 0.2)

	train_x_syn, train_y_syn = oversample(train_x, train_y)



	train_y_syn = np.array(train_y_syn)
	train_y = np.array(train_y)


	clf = MultinomialNB()
	clf.fit(train_x_syn,train_y_syn)

	prediction = clf.predict(unlabeled_vectors)
	unlabeled_tweet_ids = pickle.load(open('pickle/tweet_ids.pkl',"rb"))

	print "number of unlabled"
	print len(unlabeled_tweet_ids)
	assert len(unlabeled_tweet_ids) == unlabeled_vectors.shape[0]

	results = []

	for index,label in enumerate(prediction.tolist()):

	 	if label == 1:
	 		tweet_id = unlabeled_tweet_ids[index]

	 		tweet_id_fkey = tweet_id

	 		results.append(return_matches(tweet_id))

	 		classification = ClassifyTweet(tweet_id_fkey, class_name)
	 		query = """INSERT INTO tweet_classifications (tweet_id_fkey, classification) VALUES (%s, %s)"""
			db.insert(query, classification)
	db.connection.commit()

	# write_to_file(results, class_name)


	# print sum([label for label in prediction.tolist() if label == 1])
	#sys.exit(0)

	# print cross_validate(clf,x,y)
	# print len(x_synthetic), len(y_synthetic)
	# print cross_validate(clf,x_synthetic,y_synthetic)


	# clf.fit(x_synthetic,y_synthetic)

	# evaluate_classifier(clf,test_x,test_y,train_x_syn,train_y_syn)



	print ' NB over... no moving on to other classifiers'

	# logistic_l1 = line_search(LogisticRegression(penalty = 'l1',class_weight='auto'),x,y) 
	# svm_analysis =  line_search(svm.SVC(class_weight='auto',kernel = 'linear'),x,y) 
	# logistic_l2 = line_search(LogisticRegression(penalty = 'l2',class_weight='auto'),x,y)

	# print 'Logistic regression'
	# print logistic_l1
	# print 'SVM'
	# print svm_analysis
	# print 'LR-L2'
	# print logistic_l2


	clf_boost = Ensemble1( (train_x,train_y) )
	(f1,c_LR) = line_search(LogisticRegression(penalty = 'l1',class_weight='auto'),train_x,train_y)
	(f1,c_svm) =  line_search(svm.SVC(class_weight='auto',kernel = 'linear'),train_x,train_y) 
	
	clf_LR = LogisticRegression(penalty = 'l1',class_weight='auto',C=c_LR)
	clf_svm = svm.SVC(class_weight='auto',C=c_svm,kernel = 'linear')
	clf_NB = MultinomialNB()


	clf_boost.set_rule(LogisticRegression(penalty = 'l1',class_weight='auto',C=c_LR).fit(train_x,train_y))
	clf_boost.set_rule(svm.SVC(class_weight='auto',C=c_svm,kernel = 'linear').fit(train_x,train_y))
	clf_boost.set_rule(MultinomialNB().fit(train_x,train_y))
	prediction = clf_boost.predict(unlabeled_vectors)

	for index,label in enumerate(prediction):
	 	if label == 1:
	 		tweet_id = unlabeled_tweet_ids[index]

	 		print return_matches(tweet_id)


	# print sum([label for label in prediction if label == 1])

	# clf_boost.evaluate()
	# evaluate_classifier(clf_boost,test_x,test_y,train_x,train_y)
	# evaluate_classifier(clf,test_x,test_y,train_x,train_y)

	# classifiers=[]	
	
	#classifiers.append(clf_LR)
	#classifiers.append(clf_svm)
	#classifiers.append(clf_NB)

	# clf_adaboost = AdaBoost( (train_x,train_y) , 10)
	# clf_adaboost.make_strong_learner(classifiers)
	# print clf_adaboost.RULES
	# evaluate_classifier(clf_adaboost, test_x,test_y,train_x,train_y)
	# my_cross_validation(classifiers, x, y, 3)

if __name__ == '__main__':

	class_code = {'online_review': '2-a',
			  'past_work': '2-b',
			  'event_marketing': '2-c',
			  'channel_partnering': '2-d',
			  'webtools': '2-e',
			  'promotions': '2-f', 
			  'contact': '2-g',
			  'bragging': '2-h',
			  'environmental_impact': "1-a",
			  'investment': '1-b',
			  'govt_incentives': '1-c',
			  'pv_education': '1-d',
			  'rate_changes': '1-e',
			  'industry_growth': '1-f'}

	for class_name, code in class_code.items():
		main(class_name, code)
	# main(sys.argv[1:])
		print "done."


