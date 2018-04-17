from os import listdir
import string
from tqdm import tqdm

# load doc into memory
def load_doc(filename):
	# open the file as read only
	file = open(filename, encoding='utf-8')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text

# split a document into news story and highlights
def split_story(doc):
	# find first highlight
	index = doc.find('@highlight')
	# split into story and highlights
	story, highlights = doc[:index], doc[index:].split('@highlight')
	# strip extra white space around each highlight
	highlights = [h.strip() for h in highlights if len(h) > 0]
	return story, highlights

# load all stories in a directory
def load_stories(directory):
	#The query file opens :p
	fout = open("QueriesRaw.txt","w")
	stories = list()
	for name in tqdm(listdir(directory)):
		filename = directory + '/' + name
		# load document
		doc = load_doc(filename)
		# split into story and highlights
		story, highlights = split_story(doc)
		# store
		stories.append({'story':story, 'name':name, 'highlights':highlights})
		#print(stories[0]) ## just a check
	for triplet in tqdm(stories):
		#triplet is a dict
		queries = triplet['highlights'] #each highlight is being created as a query
		fname = triplet['name']
		for query in queries:
			fout.write(query + "\n")
	fout.close()
	return stories

# clean a list of lines
def clean_lines(lines):
	cleaned = list()
	# prepare a translation table to remove punctuation
	table = str.maketrans('', '', string.punctuation)
	for line in lines:
		# strip source cnn office if it exists
		index = line.find('(CNN) -- ')
		if index > -1:
			line = line[index+len('(CNN)'):]
		# tokenize on white space
		line = line.split()
		# convert to lower case
		line = [word.lower() for word in line]
		# remove punctuation from each token
		line = [w.translate(table) for w in line]
		# remove tokens with numbers in them
		line = [word for word in line if word.isalpha()]
		# store as string
		cleaned.append(' '.join(line))
	# remove empty strings
	cleaned = [c for c in cleaned if len(c) > 0]
	return cleaned

# load stories
directory = 'stories/'
stories = load_stories(directory)
print('Loaded Stories %d' % len(stories))

# # clean stories
# for example in stories:
# 	example['story'] = clean_lines(example['story'].split('\n'))
# 	example['highlights'] = clean_lines(example['highlights'])