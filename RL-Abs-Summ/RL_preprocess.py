from os import listdir
import string
import re
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


def sentencify(text):
	text1 = re.sub(r"((\s[A-Za-z])|Mrs|Mr|Dr|Prof|Er)\.", r"\1<$>", text)
	text2 = re.sub(r"([^!.?'][']?)\n\n", r"\1##.\n\n", text1)
	text3 = re.sub(r"(?P<sent>(?=[A-Z0-9'])([0-9]\.[0-9]|[^.!?])*)[!](?P<endquote>\'(?=\s+[a-z]))", r"\g<sent><%>\g<endquote>", text2)
	text4 = re.sub(r"(?P<sent>(?=[A-Z0-9'])([0-9]\.[0-9]|[^.!?])*)[?](?P<endquote>\'(?=\s+[a-z]))", r"\g<sent><@>\g<endquote>", text3)
	text5 = re.sub(r"(?P<sent>(?=[A-Z0-9'])([0-9]\.[0-9]|[^.!?])*[!.?]['\"]?(?=\s+[A-Z0-9']))", r'<s>\g<sent><\s>', text4)
	text6 = re.sub(r"<@>", r"?", text5)
	text7 = re.sub(r"<%>", r"!", text6)
	text8 = re.sub(r"##\.", r"", text7)
	text9 = re.sub(r"<\$>", r".", text8)
	return text9


# clean a list of lines
def clean_lines(line):
	cleaned = list()
	# prepare a translation table to remove punctuation
	table = str.maketrans('', '', string.punctuation)
	# strip source cnn office if it exists
	index = line.find('(CNN) -- ')
	if index > -1:
		line = line[index+len('(CNN)'):]

	line = sentencify(line)
	line = line.replace('<s>','')
	line = line.replace('<\s>',' delimmqm')		# delimmqm is random to ensure non-occurence in text

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
	cleaned_line = cleaned_line.replace('delimmqm','<delim>')

	cleaned_line = cleaned_line.replace('\n',' ')
	return cleaned_line 

def load_and_clean():
	# load stories
	directory = '/home/amrits/Desktop/6th_Sem/cs657/project/cnn/stories/'
	stories = load_stories(directory)
	print('Loaded Stories %d' % len(stories))

	print("Cleaning...")
	# clean stories
	for example in tqdm(stories):
		example['story'] = clean_lines(example['story'])
		example['highlights'] = clean_lines('. '.join(example['highlights'])) # concatencation of all highlights taken as summary now :)

	keys = []
	vals = []
	storyFile = open("storyFile.txt", "w")
	summFile = open("summFile.txt", "w")

	print("Writing....")
	for k in tqdm(stories):
		key = k['story']
		val = k['highlights']
		# keys.append(key)
		# vals.append(val)
		storyFile.write(key+"\n")
		summFile.write(val+"\n")
	
	# story_tuple = (keys, vals)
	# print(type(story_tuple))
	# print(type(story_tuple[0]))
	# print(type(story_tuple[0][0]))
	# save to file
	# dump(story_tuple, open('cnn_dataset.pkl', 'wb'))

	storyFile.close()
	summFile.close()

if __name__ == '__main__':
	load_and_clean()		