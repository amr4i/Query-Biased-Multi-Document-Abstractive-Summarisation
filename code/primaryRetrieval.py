import sys
import lucene
from src.retrieval import retrieve

if len(sys.argv)!=2:
	print("\nUsage: python primaryIndex.py <data_directory>\n")
	sys.exit(0)

query = sys.argv[1]

retrieved_docs = retrieve(query)

with open("retrieved_docs.txt", 'w') as f:
	for doc in retrieved_docs:
		f.write(doc+"\n")

print("Retrieved Documents are listed in retrieved_docs.txt")