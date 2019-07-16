from random import randrange as rr
from textblob import TextBlob
from random import shuffle
from json import loads

# Needs to be run once at least to get information to download books correctly
# It will take a few hours to run and complete
# from gutenberg.acquire import get_metadata_cache
# get_metadata_cache()


engBooks = ['Books/Eng/Done/1260.txt', 'Books/Eng/Done/1342.txt', 'Books/Eng/Done/330.txt', 'Books/Eng/Done/3561.txt',
			'Books/Eng/Done/3745.txt', 'Books/Eng/Done/4348.txt', 'Books/Eng/Done/4493.txt', 'Books/Eng/Done/4922.txt',
			'Books/Eng/Done/5123.txt', 'Books/Eng/Done/5338.txt', 'Books/Eng/Done/5537.txt', 'Books/Eng/Done/5893.txt',
			'Books/Eng/Done/6301.txt', 'Books/Eng/Done/7396.txt', 'Books/Eng/Done/7497.txt', 'Books/Eng/Done/7757.txt',
			'Books/Eng/Done/7759.txt', 'Books/Eng/Done/8134.txt', 'Books/Eng/Done/8862.txt', 'Books/Eng/Done/9087.txt']
freBooks = ['Books/Fre/Done/1910.txt', 'Books/Fre/Done/3456.txt', 'Books/Fre/Done/4548.txt', 'Books/Fre/Done/5096.txt',
			'Books/Fre/Done/5126.txt', 'Books/Fre/Done/6319.txt', 'Books/Fre/Done/6484.txt', 'Books/Fre/Done/6994.txt',
			'Books/Fre/Done/7173.txt', 'Books/Fre/Done/7812.txt', 'Books/Fre/Done/801.txt', 'Books/Fre/Done/8174.txt',
			'Books/Fre/Done/8186.txt', 'Books/Fre/Done/8490.txt', 'Books/Fre/Done/8739.txt', 'Books/Fre/Done/8863.txt',
			'Books/Fre/Done/9053.txt', 'Books/Fre/Done/9262.txt', 'Books/Fre/Done/9824.txt', 'Books/Fre/Done/9891.txt']
gerBooks = ['Books/Ger/Done/2229.txt', 'Books/Ger/Done/2405.txt', 'Books/Ger/Done/4504.txt', 'Books/Ger/Done/5325.txt',
			'Books/Ger/Done/6641.txt', 'Books/Ger/Done/6643.txt', 'Books/Ger/Done/6645.txt', 'Books/Ger/Done/6649.txt',
			'Books/Ger/Done/6654.txt', 'Books/Ger/Done/6822.txt', 'Books/Ger/Done/7225.txt', 'Books/Ger/Done/7859.txt',
			'Books/Ger/Done/7861.txt', 'Books/Ger/Done/7939.txt', 'Books/Ger/Done/7943.txt', 'Books/Ger/Done/7944.txt',
			'Books/Ger/Done/8927.txt', 'Books/Ger/Done/9046.txt', 'Books/Ger/Done/9108.txt', 'Books/Ger/Done/9187.txt']
allBooks = engBooks + freBooks + gerBooks


def getNBooks(nBooks, lang, loc):
	from gutenberg.acquire import load_etext
	from gutenberg.query import get_metadata
	from gutenberg.cleanup import strip_headers
	i = 0
	while i < nBooks:
		n = rr(0, 10000)
		try:
			l = get_metadata("language", n)
			# if('en' not in l):
			#     print(l)
			if (lang in l):
				t = strip_headers(load_etext(n)).strip()
				f = open(loc + str(n) + '.txt', 'w')
				f.write(t)
				f.flush()
				f.close()
				print(i + 1, n)
				i += 1
		except:
			pass


def replaceNL(file):
	f = open(file + '.txt', 'r').read().replace('\n', ' ')
	fo = open(file + '.txt', 'w')
	fo.write(f)
	fo.flush()


def getSentences(file):
	blob = TextBlob(open(file, 'r').read()).sentences
	return blob


def cleanSentence(sen):
	s = ''
	for x in sen:
		if (x.isalpha()):
			s += x
		elif (ord(x) == 710):
			pass
		elif (x in '.,!?'):
			pass
		else:
			s += ' '
	i = s.find('  ')
	while i != -1:
		s = s[:i] + s[i + 1:]
		i = s.find('  ')
	s = s.lower()
	if (len(s) > 0 and s[0] == ' '):
		s = s[1:]
	if (len(s) > 0 and s[-1] == ' '):
		s = s[:-1]
	if (len(s) > 0):
		return s
	return None


def getSentenceDict(n=160):
	d = {'Eng':[], 'Fre':[], 'Ger':[]}
	for file in allBooks:
		sens = getSentences(file)
		shuffle(sens)
		sens = sens
		p = 0
		c = 0
		try:
			while c < n:
				sen = sens[p]
				csen = cleanSentence(sen)
				if (csen != None):
					d[file[6:9]].append(csen)
					c += 1
				p += 1
		except:
			print("Ran out of values", file)

	return d


def convertDicToJsonStr(d):
	s = '{\n'
	for x in d:
		s += '\t\"' + str(x) + '\":[\n'
		for sen in d[x]:
			s += '\t\t\"' + sen + '\",\n'
		if (len(d[x]) > 1):
			s = s[:-2] + '\n'
		s += '\t],\n'
	if (len(d) > 1):
		s = s[:-2] + '\n'
	s += '}'
	return s


def getWords(s):
	return [x for x in s.split(' ') if x != '']


def writeSentencesToFile(file='Sentences.dat'):
	d = getSentenceDict()
	out = open(file, 'w')
	out.write(convertDicToJsonStr(d))
	out.flush()
	out.close()


def createWordArray(words, lets=None, maxlen=23):
	letdic = {}
	if (lets == None):
		lets = set()
		for word, l in words:
			for let in word:
				lets.add(let)
		lets = sorted(list(lets))
	for x in range(len(lets)):
		letdic[lets[x]] = x

	wordnew = []
	for word, l in words:
		i = []
		for let in word:
			i += [letdic[let]]
		i += [0] * (maxlen - len(i))
		wordnew += [(i, l)]
	return wordnew, lets


def findMax(file='Sentences.dat'):
	d = loads(open(file, 'r').read())
	m = 0
	for lang in d:
		for sen in d[lang]:
			for word in getWords(sen):
				m = max(m, len(word))
	return m
