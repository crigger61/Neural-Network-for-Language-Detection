from NeuralNetHandler import *
from bokeh.plotting import figure, show

# This is the model that I came up with that was the most accurate and most consistent. It uses the Sentences.dat and
# TestSentences.dat that are provided. Because of the way the model works, each model is locked to a certain range of
# these .dat file. It is based on the longest word found as that will determine the number of nodes in input.
# In theory it should be able to handle data with smaller longest words. But I never tested this.
s = createNN("Main",19, 3, [60, 30, 19], tr, do, step=1 / 50000, restore='NeuralNetworks/model.nnnet', saveName='NeuralNetworks/model.nnnet', numSteps=-1,saveForGraph=False)

# s= createNN("T1",19,3,[19],tr,do,step=1/20000,saveName='NeuralNetworks/Test.nnnet',restore='NeuralNetworks/Test.nnnet')
# s= createNN("T2",19,3,[30],tr,do,step=1/20000,saveName='NeuralNetworks/Test.nnnet',restore='NeuralNetworks/Test.nnnet')
# s= createNN("T3",19,3,[60],tr,do,step=1/20000,saveName='NeuralNetworks/Test.nnnet',restore='NeuralNetworks/Test.nnnet')
# s= createNN("T4",19,3,[30,30],tr,do,step=1/20000,saveName='NeuralNetworks/Test.nnnet',restore='NeuralNetworks/Test.nnnet')
# s= createNN("T5",19,3,[60,60],tr,do,step=1/20000,saveName='NeuralNetworks/Test.nnnet',restore='NeuralNetworks/Test.nnnet')
# s= createNN("T6",19,3,[30,60,30],tr,do,step=1/50000,saveName='NeuralNetworks/Test.nnnet',restore='NeuralNetworks/Test.nnnet')
# s= createNN("T8",19,3,[19,30,60,30,19],tr,do,step=1/20000,saveName='NeuralNetworks/Test.nnnet',restore='NeuralNetworks/Test.nnnet')

if (lossdata != []):
	l = []
	smoothing = 10
	for x in range(smoothing, len(lossdata)):
		sumer = 0
		for i in range(smoothing + 1):
			sumer += lossdata[x - i]
		sumer /= smoothing
		l.append((sumer))
	print("Showing graph of Loss...")

	f = figure()
	f.line(range(len(l)), l)
	show(f)
	print("Finished graphing loss...\n")

print("Generating Test data")
es = []
fs = []
gs = []

correct = {y:{0:0, 1:1} for y in [1, 2, 3]}
for x in td['Eng']:
	es += [[(i, 1) for i in getWords(x)]]
for x in td['Fre']:
	fs += [[(i, 2) for i in getWords(x)]]
for x in td['Ger']:
	gs += [[(i, 3) for i in getWords(x)]]

maxlen = findMax()
print("Generating English Test Words")
for x in range(len(es)):
	es[x] = createWordArray(es[x], lets, maxlen=maxlen)[0]
print("Generating French Test Words")
for x in range(len(fs)):
	fs[x] = createWordArray(fs[x], lets, maxlen=maxlen)[0]
print("Generating German Test Words")
for x in range(len(gs)):
	gs[x] = createWordArray(gs[x], lets, maxlen=maxlen)[0]
print("Finished Generating Test data\n")

print("Running test on all sentences in data...")
for x in es:
	if (findLangSen(testNN(*s, [i[0] for i in x]))[0] == 1):
		correct[1][1] += 1
	else:
		correct[1][0] += 1
for x in fs:
	if (findLangSen(testNN(*s, [i[0] for i in x]))[0] == 2):
		correct[2][1] += 1
	else:
		correct[2][0] += 1
for x in gs:
	if (findLangSen(testNN(*s, [i[0] for i in x]))[0] == 3):
		correct[3][1] += 1
	else:
		correct[3][0] += 1

print("Finished running testing data\n")
print("Results:")
for x in correct:
	print(['English:', 'French: ', 'German: '][x - 1], correct[x][1] / (correct[x][1] + correct[x][0]) * 100, '%')
cor = sum([correct[x][1] for x in correct])
inc = sum([correct[x][0] for x in correct])
print('Total:  ', cor / (inc + cor) * 100, '%')
