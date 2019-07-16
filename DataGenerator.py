from BookAndWordProcessor import *
from os.path import exists

print("Starting")
if (not exists('Sentences.dat')):
	print("Sentence file doesn't exist. Creating file...")
	writeSentencesToFile()
	print("Finished Generating Sentences... Longest word is {}\n".format(findMax('Sentences.dat')))

if (not exists('TestSentences.dat')):
	senlen = findMax("Sentences.dat")
	print("Test Sentence file doesn't exist. Creating file...")
	while 1:
		writeSentencesToFile('TestSentences.dat')
		print("Finished Generating Test Sentences...")
		tsenlen = findMax("TestSentences.dat")
		if (tsenlen == senlen):
			print('Max Word size matched, finishing generating\n')
			break
		else:
			print("Max Word size was not the same, size was {}. Regenerating...".format(findMax('TestSentences.dat')))

print("Reading in Sentences...")
d = loads(open('Sentences.dat', 'r').read())
print("Finished reading in Sentences...\n")

print("Reading in Test Sentences...")
td = loads(open('TestSentences.dat', 'r').read())
print("Finished reading in Test Sentences...\n")

print("Generating words and letters...")
wordsraw = set()
wordsnew = []
worddic = {'Eng':1, 'Fre':2, 'Ger':3}

for lang in d:
	for sen in d[lang]:
		for word in getWords(sen):
			wordsraw.add((word, worddic[lang]))
wordsraw = list(wordsraw)

wordsnew, lets = createWordArray(wordsraw, maxlen=findMax())
print("Finished generating words and letters...\n")

print("Generating training data and outputs for data...")
outdic = {1:[1, 0, 0], 2:[0, 1, 0], 3:[0, 0, 1]}
tr = [x[0] for x in wordsnew]
do = [outdic[x[1]] for x in wordsnew]
print("Finished generating training and outputs for data...\n")
