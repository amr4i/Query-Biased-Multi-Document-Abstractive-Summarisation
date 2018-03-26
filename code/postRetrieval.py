import sys
import lucene
from src.retrieval import retrieve
from src.indexer import indexing
from src.texttiling import textTiling
from src.redunRem import getTempDoc
from src.ExtrSent import extractSent

if len(sys.argv)!=4:
	print("\nUsage: python postRetrieval.py <data_directory> <query> <paragraphing_method>\n")
	sys.exit(0)

data_dir = sys.argv[1]
query = sys.argv[2]
p_method = int(sys.argv[3])

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

with open("RelevantDoc.txt", 'w') as f:
	for line in tempDoc:
		f.write(line)

# print tempDoc