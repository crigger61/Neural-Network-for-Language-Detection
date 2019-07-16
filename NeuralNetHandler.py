from DataGenerator import *
import tensorflow as tf
import numpy as np
lossdata = []


def createNN(n, initSize, outSize, layers, train, expected, step=.00005, restore=None, numSteps=-1,
			 saveName=None, printLoss=True, saveForGraph=False, optimize=True):
	if (saveForGraph):
		global lossdata
	print("Creating Neural Network...")

	ses = tf.InteractiveSession()
	ins = tf.placeholder(tf.float32, shape=[None, initSize])
	outs = tf.placeholder(tf.float32, shape=[None, outSize])

	weightsInit = tf.Variable(tf.truncated_normal([initSize, layers[0]]))
	biasInit = tf.Variable(tf.zeros([layers[0]]))
	layerInit = tf.nn.sigmoid(tf.matmul(ins, weightsInit) + biasInit)

	lin1 = layerInit

	for x in range(1, len(layers)):
		wi = tf.Variable(tf.truncated_normal([layers[x - 1], layers[x]]))
		bi = tf.Variable(tf.truncated_normal([layers[x]]))
		li = tf.nn.sigmoid(tf.matmul(lin1, wi) + bi)
		lin1 = li
	weightsFinal = tf.Variable(tf.truncated_normal([layers[-1], outSize]))
	biasFinal = tf.Variable(tf.zeros([outSize]))
	layerFinal = tf.nn.softmax(tf.matmul(lin1, weightsFinal) + biasFinal)

	error = 0.5 * tf.reduce_sum(tf.subtract(layerFinal, outs) * tf.subtract(layerFinal, outs))

	i = 0
	print("Finished creating Neural Network...\n")
	if (restore):
		print("Restoring previous NN...")
		try:
			tf.train.Saver().restore(ses, restore)
		except:
			print("NN Did not exist. Initializing instead...")
			ses.run(tf.initialize_all_variables())
		print("Finished restoring NN...\n")
	else:
		print("Initalizing NN...")
		ses.run(tf.initialize_all_variables())
		print("Finished initalizing NN\n")

	train_step = tf.train.GradientDescentOptimizer(step).minimize(error)
	print("Starting training...")
	if (numSteps == -1):
		print("Training until Keyboard interrupt. Press Ctrl+c to end training.")
	try:
		pl = 30000
		while numSteps == -1 or numSteps > i:

			_, loss = ses.run([train_step, error], feed_dict={ins:np.array(train), outs:np.array(expected)})
			if (printLoss):
				print(n, 'Run:', i, ' Loss:', loss, ' Changed:', pl - loss, ' Step:', step)
			if (saveForGraph):
				lossdata += [loss]
			i += 1
			if (optimize and pl - loss <= 0):
				step /= 1.1;
				del train_step
				train_step = tf.train.GradientDescentOptimizer(step).minimize(error)

			pl = loss
	except:
		if (numSteps == -1):
			print('Ended Training...')
		else:
			print("Ended Training early...")
	print("Finished training...\n")
	if (saveName != None):
		print("Saving the NN...")
		tf.train.Saver().save(ses, saveName)
		print("Finished saving the NN\n")
	print('Returning session, finalLayer, and ins...\n')
	return ses, layerFinal, ins


def testNN(ses, lf, ins, inpu):
	outs = []
	for x in inpu:
		a = ses.run(lf, feed_dict={ins:np.array([x])})[0]
		if (a[0] > a[1] and a[0] > a[2]):
			outs.append(1)
		elif (a[1] > a[0] and a[1] > a[2]):
			outs.append(2)
		else:
			outs.append(3)
	return outs


def findLangSen(lis):
	d = {x:0 for x in [1, 2, 3]}
	for x in lis:
		d[x] += 1
	if (d[1] > d[2] and d[1] > d[3]):
		return 1, 'Eng'
	elif (d[2] > d[1] and d[2] > d[3]):
		return 2, 'Fre'
	else:
		return 3, 'Ger'


def testNNSen(ses, lf, ins, inpu, l):
	a = getWords(cleanSentence(inpu))
	a = [(x, l) for x in a]
	a = createWordArray(a, lets, findMax())[0]
	a = [x[0] for x in a]
	return testNN(ses, lf, ins, a)
