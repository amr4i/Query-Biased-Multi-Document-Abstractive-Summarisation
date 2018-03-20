import sys
import lucene
from src.retrieval import retrieve
from src.indexer import indexing

if len(sys.argv)!=3:
	print("\nUsage: python primaryIndex.py <data_directory> <query>\n")
	sys.exit(0)

data_dir = sys.argv[1]
query = sys.argv[2]
indexing(data_dir) 
retrieved_docs = retrieve(query)

with open("retrieved_docs.txt", 'w') as f:
	for doc in retrieved_docs:
		f.write(doc+"\n")