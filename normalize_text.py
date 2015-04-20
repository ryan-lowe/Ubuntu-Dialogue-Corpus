import urllib
import numpy as np
import re
import csv

nicksfile = './nicks.txt'
dictfile = './emnlp_dict.txt'
words = './unknown_words.txt'
output = './fixed_words.txt'

def createNickDict(filein):
	dict1 = {}
	with open(filein, 'r') as c1:
		c1 = c1.read().split('\n')
		for word in c1:
			if word not in dict1:
				dict1[word] = 0
	return dict1

def createWordDict(filein):
	dict1 = {}
	with open(filein, 'r') as c1:
		c1 = c1.read().split('\n')
		for i in range(len(c1)):
			word = c1[i].split('\t')
			#print word
			if word[0] not in dict1 and len(word)>1:
				dict1[word[0]] = word[1]
	return dict1


#listbool indicates whether or not the input file is a list of words (vs. a block of text)
def fixWords(filein,fileout,listbool):
	nickdict = createNickDict(nicksfile)
	worddict = createWordDict(dictfile)
	wordlist = []
	numchanges = 0
	with open(filein, 'r') as c1:
		c1 = c1.read().split('\n')
		if listbool == False:
			c1 = c1.split(' ')
		for word in c1:
			if word in nickdict:
				wordlist.append(word)
			elif word in worddict:
				wordlist.append(worddict[word])
				numchanges += 1
			else:
				wordlist.append(word)
		if listbool == False:
			text = " ".join(wordlist)
	with open(fileout, 'w') as out:
		if listbool:
			for word in wordlist:
				out.write(word + '\n')
		else:
			out.write(text)
	print 'Normalization finished with ' + str(numchanges) + ' changes made.'


fixWords(words,output,True)