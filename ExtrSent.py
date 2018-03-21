import nltk
import glob
import numpy as np
#nltk.download('punkt')
from numpy import linalg as LA
import os
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as CS
from collections import Counter
from collections import defaultdict
from math import sqrt

Vocab = {} #{term:idf}
threshold = 0.2  # for CosSim
window = 3      #window for para creation
Cutoff = 3    # Top Cutoff sentences to be picked
max_gap_size = 4 #Luhn significance window
REL = 2 #How imp is relevance as cmp to fidelity in Luhn
# 100:1
LSAweight = 100.0/101.0
def clean_review(text):
# split into tokens: 
	tokens = word_tokenize(text) #list of words
# convert to lower case
	tokens = [w.lower() for w in tokens]
# remove punctuation from each word
	table = str.maketrans('', '', string.punctuation)
	stripped = [w.translate(table) for w in tokens]
# remove remaining tokens that are not alphabetic
	words = [word for word in stripped if word.isalpha()]
# filter out stop words
	stop_words = set(stopwords.words('english'))
	words = [w for w in words if not w in stop_words]
# Stemming is now done
	porter = PorterStemmer()
	stemmed = [porter.stem(word) for word in words]
	return stemmed



def CreateWindows(indices,sentences):
	GoodParas = []
	for i in indices:
		temp=""
		for x in range(max(0,i-window),min((i+window+1),len(sentences))):
			if("\n\n" in sentences[x] and x!=max(0,i-window)):
				print("Ola")
				break
			temp += sentences[x]
			temp += "\n"
		GoodParas.append(temp)
	return GoodParas
			

def CosSim(sen,query,vocab):
	sentf = Counter(sen)
	querytf = Counter(query)
	score = 0;
	norm1= 0;
	norm2 = 0;
	cnt=0
	for token in query:
		if token in sen:
			cnt+=1
			#print(token)
			#print(vocab[token])
			#print(sentf[token])
			score += vocab[token]*sentf[token]*querytf[token]*vocab[token] #tfidf of doc and tfidf of query
		norm2 += (querytf[token]*vocab[token])**2
	for token in sen:
		norm1 += (vocab[token]*sentf[token])**2

	norm1 = sqrt(norm1)
	norm2 = sqrt(norm2)

	if score == 0:
		return 0
	score = 1.0*score/(1.0*norm1*norm2)
	# print(sen)
	# print(query)
	# print(str(score) + "   " + str(cnt))
	# print("\n")
	return score

def Tfidf(sen,query,vocab):
	sentf = Counter(sen)
	querytf = Counter(query)
	score = 0;
	norm1= 0;
	norm2 = 0;
	cnt=0
	for token in query:
		if token in sen:
			cnt+=1
			#print(token)
			#print(vocab[token])
			#print(sentf[token])
			score += vocab[token]*sentf[token] #tfidf of doc and tfidf of query
		norm2 += (querytf[token]*vocab[token])**2
	for token in sen:
		norm1 += (vocab[token]*sentf[token])**2

	norm1 = sqrt(norm1)
	norm2 = sqrt(norm2)

	if score == 0:
		return 0
	#score = 1.0*score/(1.0*norm1*norm2)
	# print(sen)
	# print(query)
	# print(str(score) + "   " + str(cnt))
	# print("\n")
	return score


def ExtrSen(doc,query):
	'''Assumes doc and query are strings'''
	clean_sentences = [] # list of list of strings
	sentences = sent_tokenize(doc) # list of strings
	#print(sentences)
	word_idf = defaultdict(lambda: 0)
	word_cf = defaultdict(lambda: 0) #collection frequency
	NumDocs = len(sentences)
	for sen in sentences:
		#print(type(sen))
		clean_sent = clean_review(sen)
		words = set(clean_sent)
		for word in words:
			word_idf[word] += 1
			word_idf[word] = np.log(NumDocs*1.0 / 1.0*(1.0 + word_idf[word]))
		#print(clean_sent)
		for word in clean_sent:
			word_cf[word] +=1
		clean_sentences.append(clean_sent)

	clean_query = clean_review(query)
	print(sentences)
	VSmethod(clean_sentences,clean_query,word_idf,sentences)
	Tfidfmethod(clean_sentences,clean_query,word_idf,sentences)
	LuhnClusters(sentences,word_cf,clean_query)
	QueryBiasedLSA(clean_sentences,word_idf,clean_query,sentences)


def VSmethod(clean_sentences,clean_query,word_idf,sentences):
	print("VECTOR SPACE METHOD : \n\n")
	GoodSent = []
	for i,sen in enumerate(clean_sentences):
		score = CosSim(sen,clean_query,word_idf) #both query and sen are lists of tokens
		#print(score)
		if score >= threshold:
			GoodSent.append(i)
	#print(GoodSent)
	GoodParas = CreateWindows(GoodSent,sentences)
	for i in GoodSent:
		print(sentences[i])
		print("\n")

	#print("\n\n\n Good Paras : \n")
	# for i in GoodParas:
	# 	print(i)
	# 	print("\n")
	f = open("VectorSpaceParas.txt","w")
	for i in GoodParas:
		f.write(i)
		f.write("\n")
	f.close()

def Tfidfmethod(clean_sentences,clean_query,word_idf,sentences):
	print("TF IDF METHOD : \n\n")
	GoodSent = [] # will hold indices of the good sentences
	Scores =[]
	for i,sen in enumerate(clean_sentences):
		score = Tfidf(sen,clean_query,word_idf) #both query and sen are lists of tokens
		Scores.append(score)
	#To sort in descending order
	ind = np.argsort(-np.array(Scores))
	for i in ind[:Cutoff]:
		#print(Scores[i])
		GoodSent.append(i)
	GoodParas = CreateWindows(GoodSent,sentences)
	for i in GoodSent:
		print(sentences[i])
		print("\n")

	#print("\n\n\n Good Paras : \n")
	# for i in GoodParas:
	# 	print(i)
	# 	print("\n")
	f = open("TfidfParas.txt","w")
	for i in GoodParas:
		f.write(i)
		f.write("\n")
	f.close()

		
def LuhnClusters(sentences,word_cf,clean_query):
	print("LUHN METHOD : \n\n")
	GoodSent = [] # will hold indices of the good sentences
	#Setting threshold
	n = len(sentences)
	if n<25:
		L=25
	elif n>40:
		L=40
	if (n>=25 and n<=40):
		I=0
	else:
		I=1
	tmp = I*0.1
	if(tmp!=0):
		T = 7 + I*0.1*abs(L-n)
	else:
		T=7
	#TODO: What the fuck is up with threshold?
	T=2
	#Create significant stems
	sig_stems = []
	for token in word_cf.keys():
		if word_cf[token] >= T:
			sig_stems.append(token)
	#Two parts of the score

	#Relevance:
	RelScores = []
	#Fidelity
	LuhnScores = []
	for sentence_ in sentences:
		chunks = []
		NONSIGNIFICANT_CHUNK = [0]*max_gap_size
		in_chunk = False
		sentence=word_tokenize(sentence_)
		for order, word in enumerate(sentence):
			porter = PorterStemmer()
			stem = porter.stem(word)
	            #print(stem+ "   " + word)
	            # new chunk
			if stem in sig_stems and not in_chunk:
				in_chunk = True
				chunks.append([1])
	            # append word to chunk
			elif in_chunk:
				is_significant_word = int(stem in sig_stems)
				chunks[-1].append(is_significant_word)

	            # end of chunk
			if chunks and chunks[-1][-max_gap_size:] == NONSIGNIFICANT_CHUNK:
				in_chunk = False
		# print(chunks)
		# print(sentence_)
		# print("\n")
		ratings =[]
		for chunk in chunks:
			words_count = len(chunk)
			assert words_count > 0

			significant_words = sum(chunk)
			if significant_words == 1:
			    ratings.append(0)
			else:
			    ratings.append(significant_words**2 / words_count)
		Tmp = max(ratings) if ratings else 0
		LuhnScores.append(Tmp)
		cnt=0
		for token in clean_query:
			if token in clean_review(sentence_):
				cnt+=1
		Tmp_ = 1.0*REL*(cnt**2)/1.0*(len(clean_query))
		RelScores.append(Tmp_)

	#Calculating Relevence + Fidelity
	OverallScores = np.array(LuhnScores) + np.array(RelScores)
	ind = np.argsort(-OverallScores)
	for i in ind[:Cutoff]:
		#print(OverallScores[i])
		GoodSent.append(i)
	GoodParas = CreateWindows(GoodSent,sentences)
	for i in GoodSent:
		print(sentences[i])
		print("\n")

	#print("\n\n\n Good Paras : \n")
	# for i in GoodParas:
	# 	print(i)
	# 	print("\n")
	f = open("LuhnParas.txt","w")
	for i in GoodParas:
		f.write(i)
		f.write("\n")
	f.close()

def QueryBiasedLSA(clean_sentences,word_idf,clean_query,sentences):
	print("LSA method\n")
	GoodSent = []
	#CreateVocab
	i=0
	for word in word_idf.keys():
		word_idf[word] = i
		i+=1
	#Cvt clean_sentences to a list of strings
	for i in range(len(clean_sentences)):
		clean_sentences[i] = " ".join(clean_sentences[i])
	#To cvt queery to string
	clean_query = " ".join(clean_query)
	#formality to make it list of string so that vectorizer accepts it
	tp = []
	tp.append(clean_query)
	clean_query = tp
	#Create the sentence-term matrix : Every entry is the raw tf
	vectorizer = TfidfVectorizer(vocabulary = word_idf,norm = None,use_idf=False)
	Sen_Term_matrix = vectorizer.fit_transform(clean_sentences).toarray()
	#Sen_term_matrix is a numy nd array now
	Term_Sen_matrix =Sen_Term_matrix.T
	u, s, vT = np.linalg.svd(Term_Sen_matrix, full_matrices=True)
	print(u.shape, s.shape, vT.shape)
	#Deciding KK
	#KK will be such that the singular values do not fall below half the value of the highest singular value
	KK=1
	Cmp = s[0]*1.0/2.0
	for i in range(s.shape[0]):
		if s[i] >= Cmp:
			KK+=1
	print(KK)
	#KK=3
	print(s[0],s[1],s[2],s[3],s[4])
	Uk = u[:,:KK]
	Sk = np.diag(s[:KK])
	#print(Sk.shape)
	Vtk = vT[:KK,:]  
	Tp = np.matmul(Sk,Vtk)
	#print(len(clean_sentences))
	#print(Tp.shape[1])
	assert Tp.shape[1] == len(clean_sentences)
	#print(Tp[:,1])

	#Scoring will be in two parts

	#Accd to the paer, the LSA part
	LSAScores = np.zeros(Tp.shape[1])
	#Our modification, add a query relevance meausre
	RelScores = np.zeros(Tp.shape[1])

	Query_Term_Vec = vectorizer.fit_transform(clean_query).toarray()
	Query_Term_Vec = Query_Term_Vec.T
	Sk_ = LA.inv(Sk)
	Query_in_KK = np.matmul(np.matmul(Sk_,Uk.T),Query_Term_Vec) # KK x 1
	Query_in_KK = Query_in_KK.flatten()
	print(Query_in_KK)
	print(np.argmax(Query_in_KK))
	
	# #A new lead:
	# ind_ = np.argsort(-Query_in_KK)
	# for i in ind_[:]:
	# 	print(i)
	# 	j= np.argmax(Tp[i,:])
	# 	print(sentences[j])
	# 	print("\n")




	for i in range(Tp.shape[1]):
		LSAScores[i] = (LA.norm(Query_in_KK*Tp[:,i]))
	#print(Query_Term_Vec.shape)
	#Project query vector to LSA concept space


	
	for i in range(Tp.shape[1]):
		# # #Cvt to 2D array because CS demands so
		# # Q1 = Query_in_KK.reshape(-1,1)
		# # S1 = Tp[:,i].reshape(-1,1)
		# # print(Q1.shape, S1.shape)
		# print((CS(Q1,S1)))
		RelScores[i] = np.dot(Query_in_KK,Tp[:,i])
		RelScores[i] = 1.0*RelScores[i]/1.0*(LA.norm(Query_in_KK)*LA.norm(Tp[:,i]))
		#print(RelScores[i],LSAScores[i])
	OverallScores = LSAweight*RelScores + (1-LSAweight)*LSAScores
	ind = np.argsort(-OverallScores)
	for i in ind[:Cutoff]:
		print(OverallScores[i])
		GoodSent.append(i)
	GoodParas = CreateWindows(GoodSent,sentences)
	for i in GoodSent:
		print(sentences[i])
		print("\n")
	f = open("LSAparas.txt","w")
	for i in GoodParas:
		f.write(i)
		f.write("\n")
	f.close()


	





f= open('3topic.txt',"r+")
ExtrSen(f.read(),"What are animals")
#print(Vocab)

