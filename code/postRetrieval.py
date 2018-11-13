import sys
import lucene
import pickle
from src.retrieval import retrieve
from src.indexer import indexing
from src.texttiling import textTiling
from src.redunRem import getTempDoc
from src.ExtrSent import extractSent
from src.ExtrSent2 import extractSent as extractSent2

if len(sys.argv)!=4:
	print("\nUsage: python postRetrieval.py <data_directory> <query> <paragraphing_method> <relevanceInjectionMethod>\n")
	sys.exit(0)

'''
Relevance Injection MEthod:
1 ==> Extract relevant paras, and combine them and get a TempDoc on which we can run Abs Summm.
2 ==> Extract all sent-rel pairs for all relevant documents and create incremental abs summ from them, using redum removal 
on generated abs summaries. 
'''

data_dir = sys.argv[1]
query = sys.argv[2]
p_method = int(sys.argv[3])
relInj_method = int(sys.argv[4])

if relInj_method == 1:
	retrieved_docs = []

	with open("retrieved_docs.txt", 'r') as f:
		retrieved_docs = f.readlines()
			
	# print retrieved_docs
	if p_method == 1:
		textTiling(data_dir, retrieved_docs)
		indexing("./results")
		imp_paras = retrieve(query)
	else:
		imp_paras = extractSent(data_dir, retrieved_docs, query, p_method)

	tempDoc, tempDocVecs = getTempDoc("./results", imp_paras)

	print len(tempDoc)
	with open("RelevantDoc.txt", 'w') as f:
		for line in tempDoc:
			f.write(line)

elif relInj_method == 2:
	retrieved_docs = []

	with open("retrieved_docs.txt", 'r') as f:
		retrieved_docs = f.readlines()
			
	# print retrieved_docs
	if p_method == 1:
		print("\nCan't use TextTiling with the mentioned Relevance Injection Method.")
	else:
		allDocsSenRelPairs = extractSent(data_dir, retrieved_docs, query, p_method)

	with open("allDocsSenRelPairs.pkl", "w") as f:
		pickle.dump(allDocsSenRelPairs, f, protocol=1)


