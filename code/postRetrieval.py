import sys
import lucene
from src.retrieval import retrieve
from src.indexer import indexing
from src.texttiling import textTiling
from src.redunRem import getTempDoc

if len(sys.argv)!=3:
	print("\nUsage: python postRetrieval.py <data_directory> <query>\n")
	sys.exit(0)

data_dir = sys.argv[1]
query = sys.argv[2]

retrieved_docs = []

with open("retrieved_docs.txt", 'r') as f:
	retrieved_docs = f.readlines()
		
# print retrieved_docs

textTiling(data_dir, retrieved_docs)
indexing("./results")
imp_paras = retrieve(query)
tempDoc, tempDocVecs = getTempDoc("./results", imp_paras)

print tempDoc
# print len(tempDoc)