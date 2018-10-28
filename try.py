
import re
import string
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
	print(line)

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



text = '"You know, it surprised me, and I was rather shocked that they were there. So I took a short video and a picture of the vehicles. I didn\'t give any location out," he said.'

print(clean_lines(text))