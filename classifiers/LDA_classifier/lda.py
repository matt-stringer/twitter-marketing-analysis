import MySQLdb
import sys
from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from itertools import izip
import CMUTweetTagger

from nltk.tokenize import RegexpTokenizer


class Database:
	# host="research.czxveiixjbkr.us-east-1.rds.amazonaws.com"
	# user="user"
	# password="tw33ter12"
	# db="twitterresearch"

	host='tweets.czxveiixjbkr.us-east-1.rds.amazonaws.com'
	user='matt'
	password='pred_modeling'
	db='solar_marketing'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()


	def insert(self, query, object=None):
		try:
			if object is None:
				self.cursor.execute(query)
			# elif isinstance(object, ClassifyTweet):
			# 	self.cursor.execute(query, (object.tweet_id_fkey, object.classification))
		
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
dictionary = {}

# class MyCorpus(object):

# 	def __init__(self, result_set):
# 		self.result_set = result_set



# 	def __iter__(self):
# 		for line in self.result_set:
# 			yield dictionary.doc2bow(line.lower().split())

# corpus_memory_friendly = MyCorpus(text)





tagged_text = []

not_needed = {',': 'punctuation',
			  'U': 'hyperlink',
			  'D': '',
			  '~': 'ex - ...',
			  'G': 'just letters or symbols'}

pos_needed = {'V': "verb", 
			  'N': "noun",
			  '^': 'proper noun',
			  'P': 'preposition',
			  'R': 'adverb',
			  'A': 'ex - one-fourth',
			  '&': 'conjuction',
			  '@': '@',
			  '#': 'hashtag',
			  'O': 'pronoun',
			  'Z': 'possesive',
			  'S': 'possesive or maybe contraction',
			  'T': 'Location',
			  'L': 'contraction',
			  '$': 'number',
			  '!': 'exclamation',
			  'E': 'emoticon'}


def tag_tweets(text):
	texts = []
	tweet_stack_command = "java -XX:ParallelGCThreads=2 -Xmx500m -jar /Users/mattstringer/research/twitter-research/tweet_tags/ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar"

	for i in text:
		tagged_tweets = CMUTweetTagger.runtagger_parse(i, run_tagger_cmd=tweet_stack_command)
		tweet = []
		for tag in tagged_tweets[0]:
			if tag[1] in pos_needed.keys():
				tweet.append(tag[0].lower())
		texts.append(tweet)

	return texts

def remove_single_word_occurrence(texts):
	"""
	removes words that only occur once in the total corpus
	"""

	all_tokens = sum(texts, [])
	tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
	texts = [[word for word in text if word not in tokens_once] for text in texts]
	return texts

def make_LSA_output(dictionary, corpus, topics=2):
	tfidf = models.TfidfModel(corpus) 
	corpus_tfidf = tfidf[corpus]

	# I can print out the topics for LSA
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=topics)
	corpus_lsi = lsi[corpus]

	for l,t in izip(corpus_lsi,corpus):
	  print l,"#",t
	print 


	for top in lsi.print_topics(2):
	  print top

	lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=50)
	corpus_lda = lda[corpus]

	for l,t in izip(corpus_lda,corpus):
	  print l,"#",t
	print

	# But I am unable to print out the topics, how should i do it?
	for top in lda.print_topics(100):
	  print top


def main():

	query  = """SELECT tweet FROM tweets LIMIT 10;"""
	text = db.query(query)

	texts = tag_tweets(text)
	texts = remove_single_word_occurrence(texts)

	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]




if __name__ == "__main__":
	main()





