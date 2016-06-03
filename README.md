Twitter Analysis
================


# Project Objective:

This project takes solar installer Tweets to better understand and classify their marketing strategies. As Tweets have a time stamp, the looks to use their timestamp to better understand the change over time of their marketing strategies. The 


# Process
* Import tweets from the top US residential solar installers to an SQL database
* Tag Tweets manually to better understand and classify tweets.
*  Apply Natural Language Processing (NLP) tools to process the text data for each company's description: word tokenization, TFIDF
* Condense terms using Non-negative matrix factorization (NMF) for topic modeling
* Assign TFIDF term scores and NMF topic scores to each business and investor (average scores across all companies invested in)
* Use cosine distance as a metric to measure similarity between solar installers



### dependencies
Scripts were written in Python 2.7. You'll need the following modules: 
```bash
matplotlib >= 1.5.1  
nltk >= 3.1
numpy >= 1.10.1  
pandas >= 0.17.1  
python-dateutil >= 2.4.2
scipy >= 0.16.0
seaborn >= 0.6.0
sklearn >= 0.17
spacy >= 0.100
statsmodels >= 0.6.1
pattern >= 2.6
vaderSentiment 
```

To install modules, run:  
```bash
$ pip install <module>
```

### running

