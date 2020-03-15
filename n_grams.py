# Importing libraries 
import sys
import nltk 
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import pandas as pd 
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Input the file 
txt1 = [] 
file_path = sys.argv[1]
with open(file_path) as file: 
	txt1 = file.readlines() 


# Lemmatize

wordnet_lemmatizer = WordNetLemmatizer()
def lemmatizing(text):
    word_tokens = word_tokenize(text)
    lemmatized_word = [wordnet_lemmatizer.lemmatize(word) for word in word_tokens]
    return ' '.join(s for s in lemmatized_word)

# Stemming
porter_stemmer = PorterStemmer()
def stemming(text):
    word_tokens = nltk.word_tokenize(text)
    stemmed_word = [porter_stemmer.stem(word) for word in word_tokens]
    return ' '.join(s for s in stemmed_word)



# Preprocessing 
def remove_string_special_characters(s): 
	
	# removes special characters without alphabetic and digit
	stripped = re.sub('[^a-zA-z\s()0-9]', '', s) 
	stripped = re.sub('_', '', stripped) 
	
	# Change any white space to one space 
	stripped = re.sub('\s+', ' ', stripped) 
	
	# Remove start and end white spaces 
	stripped = stripped.strip() 
	# Lower text
	if stripped != '': 
			return stripped.lower() 
		
# Stopword removal 
stop_words = set(stopwords.words('english')) 
your_list = ['data', 'science'] 
for i, line in enumerate(txt1): 
    line = remove_string_special_characters(line)
    line = lemmatizing(line)
    # line = stemming(line)
    txt1[i] = ' '.join([x for
		x in nltk.word_tokenize(line) if
		( x not in stop_words ) and ( x not in your_list )]) 

# Write the text into file
output_file = open("new.txt", 'w', encoding='utf-8')
output_file.writelines(txt1)
output_file.close()
# Getting bi-grams
vectorizer = CountVectorizer(ngram_range = (2,2)) 
X1 = vectorizer.fit_transform(txt1) 
features = (vectorizer.get_feature_names()) 
# print("\n\nFeatures : \n", features) 
# print("\n\nX1 : \n", X1.toarray()) 

# Applying TFIDF for scoring
vectorizer = TfidfVectorizer(ngram_range = (2,2)) 
X2 = vectorizer.fit_transform(txt1) 
scores = (X2.toarray()) 
# print("\n\nScores : \n", scores) 

# Getting top ranking features 
sums = X2.sum(axis = 0) 
data1 = [] 
for col, term in enumerate(features): 
	data1.append( (term, sums[0,col] )) 
ranking = pd.DataFrame(data1, columns = ['term','rank']) 
words = (ranking.sort_values('rank', ascending = False)) 
print ("\n\nWords head : \n", words.head(10)) 

WC_height = 500
WC_width = 1000
WC_max_words = 100

# build the dict for wordcloud
word_dicts = {}
for feature in data1:
    word_dicts['_'.join(feature[0].split())] = feature[1]

wordCloud = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width)
 
wordCloud.generate_from_frequencies(word_dicts)
 
plt.title('Most frequently occurring bigrams')
plt.imshow(wordCloud, interpolation='bilinear')
plt.axis("off")
plt.show()


