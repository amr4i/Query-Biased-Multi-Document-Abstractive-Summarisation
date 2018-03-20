import os
from math import sqrt
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def cos_sim(dict_a, dict_b):
	num=0
	den=0
	mod_a=0
	mod_b=0
	for i in dict_a:
		if i in dict_b:
			num = num + dict_a[i]*dict_b[i]
	for i in dict_a:
		mod_a = mod_a+dict_a[i]*dict_a[i]
	for i in dict_b:
		mod_b = mod_b+dict_b[i]*dict_b[i]
	mod_a = sqrt(mod_a)
	mod_b = sqrt(mod_b)
	den = mod_a*mod_b
	return num*1.0/den

corpus = []
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

threshold = 0.5



def getTempDoc(directory, file_list=None):

	temp_doc = []
	temp_doc_vecs = []
	doc_num = 0
	total_num_sent = 0

	if file_list == None:
		file_list = os.listdir(directory)

	# print file_list

	for file in file_list:
		file = file.split('/')[-1]
		with open(os.path.join(directory,file), 'r') as f:
			doc_num = doc_num + 1
			text = f.read()
			sent_list = sent_tokenize(text)
			doc_vec = []
			doc = []
			
			for sent in sent_list:
				word_list = word_tokenize(sent)
				filtered_words = [ps.stem(w) for w in word_list if not w in stop_words]
				sent_vec = {}
				total_num_sent +=1
				
				for word in filtered_words:
					if not word in corpus:
						corpus.append(word)
					word_index = corpus.index(word)
					if word_index in sent_vec:
						sent_vec[word_index] = sent_vec[word_index]+1
					else:	
						sent_vec[word_index] = 1
				
				if doc_num == 1:
					temp_doc.append(sent)
					temp_doc_vecs.append(sent_vec)
				else:
					flag=1
					for vec_dict in temp_doc_vecs:
						if cos_sim(vec_dict, sent_vec) >= threshold:
							flag = 0
					if flag==1:
						doc_vec.append(sent_vec)
						doc.append(sent_list.index(sent))

			for i in range(0, len(doc)):
				temp_doc.append(sent_list[doc[i]])
				temp_doc_vecs.append(doc_vec[i])
			
	dim = len(corpus)

	return temp_doc, temp_doc_vecs

if __name__ == '__main__':
	if len(sys.argv) == 1:
		getTempDoc('./results')
	elif len(sys.argv) == 2:
		getTempDoc(sys.argv[1])
	elif len(sys.argv) == 3:
		getTempDoc(sys.argv[1], sys.argv[2])
	else:
		print "Please input in correct foramt."

