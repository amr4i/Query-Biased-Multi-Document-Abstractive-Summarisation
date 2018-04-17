from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from tqdm import tqdm
import string
import _pickle as pickle

# create English stop words list
en_stop = set(stopwords.words('english'))

# Create p_stemmer of class PorterStemmer
    
# create sample documents
f = open("QueriesRaw.txt","r+")
text = f.readlines()
# doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
# doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
# doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
# doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
# doc_e = "Health professionals say that brocolli is good for your health." 

# compile sample documents into a list
doc_set = text

# list for tokenized documents in loop
texts = []

# loop through document list
for i in tqdm(doc_set):
    
    # split into tokens: 
	tokens = word_tokenize(i) #list of words
	# print(tokens[:100])
	# convert to lower case
	tokens = [w.lower() for w in tokens]
	# remove punctuation from each word
	table = str.maketrans('', '', string.punctuation)
	stripped = [w.translate(table) for w in tokens]
	# remove remaining tokens that are not alphabetic
	words = [word for word in stripped if word.isalpha()]
	#remove stop-words
	stop_words = set(stopwords.words('english'))
	words = [w for w in words if not w in stop_words]
	texts.append(words)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
print("Generating model.................")
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=50, id2word = dictionary, passes=500)
topicWords = ldamodel.print_topics(num_topics=50, num_words=6)
print("Saving model to file...........")

for i in topicWords:
	print(i)

pickle_out = open("LDA_500" + ".pickle","wb")
pickle.dump(topicWords, pickle_out)
pickle_out.close()
