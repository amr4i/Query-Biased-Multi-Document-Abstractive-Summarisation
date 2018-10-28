file1 = open("../storyFile.txt", "r+")
file2 = open("../summFile.txt", "r+")

stories = file1.readlines()
summs = file2.readlines()

num_stories = len(stories)

trainLen = int(0.8*num_stories)
train1 = stories[:trainLen]
train2 = summs[:trainLen]

DevEnd = int(0.9*num_stories)
dev1 = stories[trainLen:DevEnd]
dev2 = summs[trainLen:DevEnd]

test1 = stories[DevEnd:]
test2 = summs[DevEnd:]

names = ["data/train_story", "data/train_summ", "data/dev_story", "data/dev_summ", "data/test_story", "data/test_summ"]
names2 = [train1, train2, dev1, dev2, test1, test2]

for n in names:
	f = open(n, "w")
	for l in names2[names.index(n)]:
		f.write(l)
	f.close()