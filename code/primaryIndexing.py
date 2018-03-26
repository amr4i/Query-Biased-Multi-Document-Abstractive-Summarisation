import sys
import lucene
from src.indexer import indexing

if len(sys.argv)!=2:
	print("\nUsage: python primaryIndex.py <data_directory>\n")
	sys.exit(0)

data_dir = sys.argv[1]

indexing(data_dir) 
print("Indexing Done.")