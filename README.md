Twitter Analysis
================


# Project Objective:

This project takes solar installer Tweets to better understand and classify their marketing strategies. The analysis utilizes tf-idf weighting, k-means clustering, and topic modeling/LDA to determine key topics solar installer marketing. As tweets have a time reference, we look for trends in marketing over time across both the entire industry and among individual companies. 

## in this repo
* `scrape_teets/` python script to get tweets from solar installer twitter accounts
* `Solar Marketing Analysis.ipynb` jupyter notebook with scripts and outputs for text processing, k-means clustering and topic modeling
* `data/` contains data and script for analysis
* `analysis/` future analysis to be integrated into online analysis


# Process
* Import tweets from the top US residential solar installers to an SQL database
* Manually tag tweet to better understand and classify tweets.
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

