import MySQLdb
import logging
import CMUTweetTagger
import unicodedata
from decimal import *

tweet_stack_command = "java -XX:ParallelGCThreads=2 -Xmx500m -jar /Users/mattstringer/Downloads/ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar"

class Database:
	# host="research.czxveiixjbkr.us-east-1.rds.amazonaws.com"
	# user="user"
	# password="tw33ter12"
	# db="twitterresearch"

	host='localhost'
	user='root'
	password='yourpassword'
	db='twitterresearch'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()

	def query(self, query):
		try:
			self.cursor.execute(query)
			return self.cursor.fetchall()

		except Exception as e:
			print sys.exc_info()
			print "broken"

# index inverter found here - https://github.com/matteobertozzi/blog-code/blob/master/py-inverted-index/invindex.py
_WORD_MIN_LENGTH = 3
_STOP_WORDS = frozenset([
'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 
'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been', 
'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 
'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can', 
'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 
'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 
'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 
'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 
'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 
'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 
'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 
'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 
'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 
'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 
'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 
'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 
'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 
'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 
'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 
'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 
'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 
'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 
'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 
'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 
'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 
'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 
'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 
'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
'yourselves', 'the'])


def word_split(text):
	word_list = []
	wcurrent = []
	windex = None

	for i, c in enumerate(text):
		# finds out if it is alphanumeric
		if c.isalnum():
			wcurrent.append(c)
			windex = i
		elif wcurrent:
			word = u''.join(wcurrent)
			word_list.append((windex - len(word) + 1, word))
			wcurrent = []

	if wcurrent:
		word = u''.join(wcurrent)
		word_list.append((windex - len(word) + 1, word ))

	return word_list

def words_cleanup(words):
	
	cleaned_words = []
	for index, word in words:
		if len(word) < _WORD_MIN_LENGTH or word in _STOP_WORDS:
			continue
		cleaned_words.append((index, word))
	return cleaned_words

def words_normalize(words):
	"""
	Maybe I should also remove hash tags
	"""
	normalized_words = []
	for index, word in words:
		wnormalized = word.lower()
		normalized_words.append((index, wnormalized))
	return normalized_words

def word_index(text):
	words = word_split(text)
	words = words_normalize(text)
	words = words_cleanup(text)
	return words

def inverted_index(text):
	"""
	an helper, take an input text and does all the word 
	splitting/normalization job and the result is a list 
	of tuple that contains position and word. 
	[(1, u'niners'), (13, u'coach')].
	"""
	inverted = {}

	for index, word in word_index(text):
		tweet_reference = inverted.setdefault(word, [])
		tweet_reference.append(index)
	return inverted

def inverted_index_add(inverted, doc_id, doc_index):
	"""
	returns a dictionary with words as keys and 
	locations (position of the words in the document) as values.
	"""
	for word, tweet_reference in doc_index.iteritems():
		indices = inverted.setdefault(word, {})
		indices[doc_id] = tweet_reference
	return inverted

def search(inverted, query):
	words = [word for _, word in word_index(query) if word in inverted]
	results = [set(inverted[word].keys()) for word in words]
	return reduce(lambda x, y: x & y, results) if results else []


db = Database()

tweets = """SELECT tweets.tweet_id, tweets.tweet, accounts.company, accounts.screen_name FROM tweets
				INNER JOIN accounts on tweets.twitter_id_fkey = accounts.twitter_id
				LIMIT 100;"""

tweets = db.query(tweets)

# for location in locations:
# 	print location[0], location[3], location[4]

documents = {}
inverted = {}

for tweet in tweets:
	tweet_text = tweet[1]
	documents[tweet[0]] = tweet_text.decode('ascii', 'ignore')
	# for doc_id, text in documents.iteritems():
	# 	doc_index = inverted_index(text)
	# 	print doc_index
	unicode_ignore = tweet[1].decode('ascii', 'ignore')
	word_list = CMUTweetTagger.runtagger_parse([unicode_ignore], run_tagger_cmd=tweet_stack_command)


	# nouns = [word[0] for word in word_list[0] if word[1] ==  'N']
	proper_nouns = [word[0] for word in word_list[0] if word[1] == '^']
	# words = [word[0] for word in word_list[0]]


	previous_proper_noun = " "
	previous_result = ()
	search_proper_noun = ""
	end = 1
	start = 0
	print proper_nouns

	while end <= len(proper_nouns):
		search_string = " ".join(proper_nouns[start:end])
		print search_string
		query = u"""SELECT gazetikiid, name, asciiname, alternatenames, latitude, longitude FROM ca_locations WHERE name LIKE %s AND longitude > 1"""
		args = [u"%{this_name}%".format(this_name= search_string)] 
		db.cursor.execute(query, args)
		location = db.cursor.fetchall()

		if len(location) > 0:
			end += 1
			print "hit"
			
		else:
			if start == 0 and end == 1:
				start = end
				end += 1
			
			elif end == len(proper_nouns) and start == (end - 1):
				print "break 1"
				start += 1
				end += 1


			elif start == (end - 1):
				print "break 2"
				start += 1
				end += 1


			else:
				start = end - 1
				end = start + 1


			
			print "miss"
		
		print location
	# for proper_noun in proper_nouns:
		

	# 	search_proper_noun = search_proper_noun + proper_noun + " "
	# 	print search_proper_noun[0:-1]
	# 	# print len(search_proper_noun)
	# 	query = u"""SELECT gazetikiid, name, asciiname, alternatenames, latitude, longitude FROM ca_locations WHERE name LIKE %s"""
	# 	args = [u"%{this_name}%".format(this_name= search_proper_noun[0:-1])] 
	# 	db.cursor.execute(query, args)
	# 	location = db.cursor.fetchall()
	# 	# print location
	# 	# print len(location)
	# 	if len(location) > 0:
	# 		previous_proper_noun = search_proper_noun
	# 		previous_result = location
	# 	else:
	# 		search_proper_noun = ""

	# print previous_proper_noun


	# print [word for word in word_list if len(word) == maxlen]
	# for word in word_list[0]:
	# 	print word[0], word[1]