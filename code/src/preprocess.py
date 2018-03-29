from os import listdir
import string
from pickle import dump
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
	stories = list()
	for name in tqdm(listdir(directory)):
		filename = directory + '/' + name
		# load document
		doc = load_doc(filename)
		# split into story and highlights
		story, highlights = split_story(doc)
		# store
		stories.append({'story':story, 'highlights':highlights})
		# break
	return stories

# clean a list of lines
def clean_lines(line):
	cleaned = list()
	# prepare a translation table to remove punctuation
	table = str.maketrans('', '', string.punctuation)
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
	cleaned_line = ' '.join(line)
	# remove empty strings
	# cleaned = [c for c in cleaned if len(c) > 0]
	return cleaned_line

def load_and_clean():
	# load stories
	directory = '/home/amrits/Desktop/cs657/project/cnn/stories/'
	stories = load_stories(directory)
	print('Loaded Stories %d' % len(stories))

	# clean stories
	for example in stories:
		example['story'] = clean_lines(example['story'])
		example['highlights'] = clean_lines(example['highlights'][0])

	keys = []
	vals = []
	for k in stories:
		key = k['story']
		val = k['highlights']
		keys.append(key)
		vals.append(val)
	
	story_tuple = (keys, vals)
	# print(type(story_tuple))
	# print(type(story_tuple[0]))
	# print(type(story_tuple[0][0]))
	# save to file
	dump(story_tuple, open('cnn_dataset.pkl', 'wb'))

if __name__ == '__main__':
	load_and_clean()		