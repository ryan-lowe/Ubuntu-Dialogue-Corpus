from __future__ import division
import math
from random import randint
from random import shuffle
import time
import os
import csv
import sys
import nltk
from nltk.corpus import wordnet as wn
from sklearn.externals import joblib

def read_random_line(f, chunk_size=128): #optimization that is currently not used
    import random
    with open(f, 'rb') as f_handle:
        f_handle.seek(0, os.SEEK_END)
        size = f_handle.tell()
        i = random.randint(0, size)
        while True:
            i -= chunk_size
            if i < 0:
                chunk_size += i
                i = 0
            f_handle.seek(i, os.SEEK_SET)
            chunk = f_handle.read(chunk_size)
            i_newline = chunk.rfind(b'\n')
            if i_newline != -1:
                i += i_newline + 1
                break
            if i == 0:
                break
        f_handle.seek(i, os.SEEK_SET)
        return f_handle.readline()

def clean_str(c2): #generates the list of utterances from the file
  #c2 = c1.read().split('\n')
  utterlist = []
  for row in c2:
    row = row.split('\t')
    if row[0] == 'ubotu' or row[0] == 'ubottu' or row[0] == 'ubot3':
      return [0,0]
    if len("".join(row[3:])) != 0:
      utterlist.append("".join(row[3:]))
  return utterlist

def getUserList(c2):
  userlist = []
  for row in c2:
    row = row.split('\t')
    if row[0] == 'ubotu' or row[0] == 'ubottu' or row[0] == 'ubot3':
      return [0,0]
    if len("".join(row[3:])) != 0:
      userlist.append(row[1])
  return userlist  

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def checkValidity(c2, percentage, convo): #checks whether we accept or reject a file
  #c2 = c1.read().split('\n')
  userlist = []
  uniqueuser = {}
  for row in c2:
    row = row.split('\t')
    if len(row)>1:
      if len(row[1]) != 0:
        userlist.append(row[1])
        if row[1] not in uniqueuser:
          uniqueuser[row[1]] = 1
        else:
          uniqueuser[row[1]] += 1
  for user,value in uniqueuser.iteritems():
    if value < percentage*len(userlist) and len(userlist) >= 1:
      return False
      self.writeFiles('../deletedfiles.csv', [convo])
  return True

def diff_times_in_seconds(t1,t2,date1,date2):
  t1 = t1.split(':')
  t2 = t2.split(':')
  date1 = date1.split('-')
  date2 = date2.split('-')
  if len(t1)<2 or len(t2)<2 or len(date1)<3 or len(date2)<3:
    return 60*60*24 #return 1 day if something goes wrong
  if not is_number(t1[0]) or not is_number(t1[1]) or not is_number(t2[0]) or not is_number(t2[1]):
    return 60*60*24
  if not is_number(date1[0]) or not is_number(date1[1]) or not is_number(date1[2]) or not is_number(date2[0]) or not is_number(date2[1]) or not is_number(date2[2]):
    return 60*60*24
  h1,m1,s1 = int(t1[0]),int(t1[1]),0#int(t1[2])
  h2,m2,s2 = int(t2[0]),int(t2[1]),0#int(t2[2])
  d1,mo1,yr1 = int(date1[2]),int(date1[1]),int(date1[0])
  d2,mo2,yr2 = int(date2[2]),int(date2[1]),int(date2[0])
  t1_secs = s1 + 60*(m1 + 60*(h1 + 24*(d1+ 30*(mo1+12*yr1))))
  t2_secs = s2 + 60*(m2 + 60*(h2 + 24*(d2+ 30*(mo2+12*yr2))))
  return t2_secs - t1_secs







"""#text = 'Bob \t s1 \n Joe \t s2 \n Joe \t s3 \n Joe \t s3\n Joe \t s3\n Joe \t s3\n Joe \t s3\n Joe \t s3\n Joe \t s3'
path = './dialogs/20/10905.tsv'
with open(path) as c1:
  makeTimeArray(c1)
  #print checkValidity(c1,0.2)
"""
"""
class NormalizeData:

  def __init__(self, readpath, writepath):
    self.normdict = {}
    self.readpath = readpath
    self.folders = [f for f in os.listdir(self.readpath)]
    self.writepath = writepath

  def createNormDict(self, data):
    data = re.split('\n',data)
    for row in data:
      row = re.split('\t',row)
      if row[0] not in self.normdict:
        self.normdict[row[0]] = row[1]
  
  def normalize(self, ndata, data, select):
    createNormDict(ndata)
    for folder in self.folders:
      if select == False or int(folder) == 42:
        print '   Starting ' + folder + ' folder'
        filepath = self.path + folder
        files = [f for f in os.listdir(filepath)]
        k=0
        for convo in files:
          k+=1
          if k%100 == 0:
            print 'Finished ' + str(k) + 'files'
          filein = filepath + '/' + convo
          with open(filein,'r') as c1:
            #c2 = c1.read()
            #c3 = re.split('\n',c2)#csv.reader(c1, delimiter='\t')
            #utterlist = []
            #for row in c3:
            #  row = re.split('\t',row)
            #  utterlist.append("".join(row[3:]))
            utterlist = clean_str(c1)
            for i in xrange(len(utterlist)):
              utterlist[i] = re.split(' ',utterlist[i])
              for j in xrange(len(utterlist[i])):
                if utterlist[i][j] in normdict:
                  utterlist[i][j] = normdict[utterlist[i][j]]
              utterlist[i] = " ".join(utterlist[i])
"""            


def replace_sentence(text):
    words = nltk.word_tokenize(text)
    sent = nltk.pos_tag(words)
    chunks = nltk.ne_chunk(sent, binary=False)
    sentence = []
    nodelist = ['PERSON','ORGANIZATION','GPE','LOCATION','FACILITY','GSP']
    for c,word in zip(chunks,words):
        changed = False
        if hasattr(c, 'node'):     
            if c.node in nodelist:
                sentence.append("**%s**" % c.node) 
                changed = True
        if not changed:
          if word.startswith('http://') or word.startswith('https://'):
              sentence.append("**URL**")
          elif is_number(word):
              sentence.append("**NUMBER**")
          elif os.path.isabs(word):
              sentence.append("**PATH**")
          else:
            sentence.append(word)           
    return " ".join(sentence)            

"""
path1 = './dialogs/20/10800.tsv'
pathwrite = './'
with open(path1,'r') as c1:
  c1 = c1.read()
edit = replace_sentence(c1)
#print c1
#print "-----------------------------------------------"
#print edit
sentence = "john is ryan is Kevin is Bob is Steve is Jacob"
print replace_sentence(sentence)
"""

class CreateDataset:

  def __init__(self,path):
    self.timelist = []
    self.turnlist = []

    self.traindic = {}
    self.valdic = {}
    self.testdic = {}
    self.filelist = []
    self.path = path
    self.folders = [f for f in os.listdir(self.path)]

  def makeTimeList(self, c2):
    #print c1
    #c2 = c1.read().split('\n')
    firstind = 0
    firstval = c2[0].split('\t')[0]
    while len(firstval.split('T'))<2:
      firstind += 1
      firstval = c2[firstind].split('\t')[0]
    lastind = -2
    lastval = c2[-2].split('\t')[0]
    while len(lastval.split('T')) <2:
      lastind -= 1
      lastval = c2[lastind].split('\t')[0]    
    #if len(firstval.split('T')) < 2 or len(lastval.split('T')) <2:
    #  print firstval
    #  print lastval
    firstdate = firstval.split('T')[0]
    firsttime = firstval.split('T')[1].split('Z')[0]
    lastdate = lastval.split('T')[0]
    lasttime = lastval.split('T')[1].split('Z')[0]
    timediff = diff_times_in_seconds(firsttime,lasttime,firstdate,lastdate)
    self.timelist.append(timediff)    

  def generateResponses(self, num_responses, convo, testpct):
    fakes = []
    i = 0
    while i < num_responses:
    #for i in xrange(num_responses):
      if convo in self.traindic:
        num = randint(0,int(len(self.filelist)*(1-2*testpct))-1)
        fakefile = self.path + self.filelist[num][1] + '/' + self.filelist[num][0]
      elif convo in self.valdic:
        num = randint(int(len(self.filelist)*(1-2*testpct)),int(len(self.filelist)*(1-testpct))-1)
        fakefile = self.path + self.filelist[num][1] + '/' + self.filelist[num][0]
      else:
        num = randint(int(len(self.filelist)*(1-testpct)),len(self.filelist)-1)
        fakefile = self.path + self.filelist[num][1] + '/' + self.filelist[num][0]
      #fakes.append(read_random_line(fakefile).split('\t')[3:]) 
      with open(fakefile,'r') as c1:
        utterlist = clean_str(c1)
        #c = c1.read().split('\n')
        #c = c[randint(0,len(c)-1)].split('\t')
        #c2 = "".join(c[3:])
        #c2 = c2.strip()
        c2 = utterlist[randint(0,len(utterlist)-1)].strip()
        if len(c2) > 1:
          fakes.append(c2)
          i += 1
    return fakes

  def createDicts(self, testpct, trainfiles = None, valfiles = None, testfiles = None):
    print 'Creating dictionary of training, validation, and test sets'
    if trainfiles == None:
      for folder in self.folders:
        if int(folder) > 2:
          filepath = self.path + folder
          for f in os.listdir(filepath):
            self.filelist.append([f, folder])
      shuffle(self.filelist)
      for i in xrange(int(len(self.filelist)*(1-2*testpct))):
        self.traindic[self.filelist[i][0]] = self.filelist[i][1]
        self.writeFiles('../trainfiles.csv', [self.filelist[i]])
      for i in xrange(int(len(self.filelist)*(1-2*testpct)),int(len(self.filelist)*(1-testpct))): 
        self.valdic[self.filelist[i][0]] = self.filelist[i][1]
        #self.writeFiles('../valfiles.csv', [self.filelist[i]])
      for i in xrange(int(len(self.filelist)*(1-testpct)),len(self.filelist)):
        self.testdic[self.filelist[i][0]] = self.filelist[i][1]  
        #self.writeFiles('../testfiles.csv', [self.filelist[i]])
    else:
      with open(trainfiles,'r') as c1:
        c1 = c1.read()
        for f,folder in c1:
          self.filelist.append([f,folder])
          self.traindic[f] = folder
      with open(valfiles,'r') as c1:
        c1 = c1.read()
        for f,folder in c1:
          self.filelist.append([f,folder])
          self.traindic[f] = folder
      with open(testfiles,'r') as c1:
        c1 = c1.read()
        for f,folder in c1:
          self.filelist.append([f,folder])
          self.traindic[f] = folder  
    

  def writeFiles(self, filename, data, listbool=False):
    csvname = self.path + filename
    with open(csvname,'a+') as out:
      csv_out = csv.writer(out)
      for row in data:
        if listbool:
          for col in row:
            csv_out.writerow(col)
        else:
          csv_out.writerow(row)
  
  def concatUtter(self, utterlist,userlist):
    utterlist_new = []
    i = 0
    while i<len(utterlist):
      utter = utterlist[i]
      if i == len(utterlist) - 1:
        utterlist_new.append(utter)
        break
      j = i+1
      while userlist[i] == userlist[j] and j<len(userlist):
        utter = utter + joinsentence + utterlist[j]
        j += 1
        if j == len(userlist):
          break
      i = j
      utterlist_new.append(utter)
    return utterlist_new

  def sortFiles(self, max_context_size=20, num_options_train=2, num_options_test=2, testpct=0.1, filesperprint=100, elimpct=0.2, badfiles=False):        
    self.createDicts(testpct)
    print 'Finished dictionaries, making data files'
    firstline = [['Context','Response','Correct']]
    self.writeFiles('../trainset.csv', firstline)
    self.writeFiles('../valset.csv', firstline)
    self.writeFiles('../testset.csv', firstline)    
    trainexamples = 0
    testexamples = 0
    valexamples = 0
    traindata = []
    valdata = []
    testdata = []         
    for folder in self.folders:     
      if int(folder) > 2:
        print '   Starting ' + folder + ' folder'
        filepath = self.path + folder
        files = [f for f in os.listdir(filepath)]
        k=0
        for convo in files:
          #print convo
          k+=1
          if k%100 == 0:
            print 'Finished ' + str(k) + 'files'
          #if k % 1000 == 0:
          #    break
          filein = filepath + '/' + convo
          with open(filein,'r') as c1:
            ctemp = c1
            c2 = c1.read().split('\n')
            utterlist = clean_str(c2)
            userlist = getUserList(c2)

            if  badfiles: #for making badfiles.csv   
              utterlist = []
              namedict = {}
              for row in c2:
                row = row.split('\t')
                if len("".join(row[3:])) != 0:
                  utterlist.append("".join(row[3:]))
                if len(row) < 4 and len(row[0]) != 0:
                  namedict['error'] = 0
                if len(row) > 3:
                  if len(row[2]) != 0:
                    namedict[row[2]] = 0
                  namedict[row[1]] = 0
                  if len(row[1]) == 0:
                    namedict['error'] = 0
              if len(namedict) > 2:
                self.writeFiles('../badfiles.csv', [[filein]])  
                                     
            utterlist_orig = utterlist
            for i in xrange(len(utterlist)): #parses each sentence
              utterlist[i] = replace_sentence(utterlist[i])
            
            if checkValidity(c2,elimpct,convo):
              #print utterlist
              utterlist = self.concatUtter(utterlist,userlist)
              if len(utterlist)<3:
                #print convo
                #print utterlist
                self.writeFiles('../badfiles.csv',[[convo]])
              else:
                if utterlist[0] != utterlist[1]: #checks for ubotu utterance, and for 'good' dialogue           
                  self.turnlist.append(len(utterlist))
                  self.makeTimeList(c2)
                  if convo in self.traindic:
                    for i in xrange(2,len(utterlist) - 1):
                      context = utterlist[max(0,i - max_context_size):i]
                      context = joinstring.join(context)  
                      response = utterlist[i]
                      fakes = self.generateResponses(num_options_train - 1, convo, testpct)  
                      data = [[context, response, 1]]
                      for fake in fakes:
                        data.append([context, fake, 0])
                      traindata.append(data)
                  else:
                  
                  #generate a context window size, following the approximate distribution of the training set
                    contextsize = int((max_context_size*10)/randint(max_context_size/2,max_context_size*10)) + 1 + 1 #last +1 for prediction sentence
                    if contextsize > len(utterlist):
                      contextsize = len(utterlist)
                    for i in xrange(0,int((len(utterlist))/contextsize)):
                      j = i*contextsize
                      context = utterlist[j:j + contextsize - 1]
                      context = joinstring.join(context)  
                      response = utterlist[j + contextsize - 1]
                      fakes = self.generateResponses(num_options_test - 1, convo, testpct)  
                      data = [[context, response, 1]]  
                      for fake in fakes:                  
                        data.append([context, fake, 0])              
                      if convo in self.valdic: 
                        valdata.append(data)
                        self.writeFiles('../valfiles.csv', [[convo,contextsize-1]])
                      else: 
                        testdata.append(data)
                        self.writeFiles('../testfiles.csv', [[convo,contextsize-1]])
              if k % filesperprint == 0 or k == len(files):
                if traindata != []:
                  self.writeFiles('../trainset.csv', traindata, listbool=True)
                if valdata != []:
                  self.writeFiles('../valset.csv', valdata, listbool=True)
                if testdata != []:
                  self.writeFiles('../testset.csv', testdata, listbool=True)
                traindata = []
                valdata = []
                testdata = []
    self.writeFiles('../timelist.csv',[timelist])
    self.writeFiles('../turnlist.csv',[turnlist])


global joinstring 
global joinsentence
joinstring = ' </s> '
joinsentence = '. '
data1 = CreateDataset('./dialogs/')
data1.sortFiles()

#data1.sortFiles(20,2,2,0.1,50,False)
"""
def makeTimeList(c2):
  #print c1
  #c2 = c1.read().split('\n')
  print c2
  firstval = c2[0].split('\t')[0]
  lastval = c2[-2].split('\t')[0]
  if len(firstval.split('T')) ==1 or len(lastval.split('T')) ==1:
    print firstval
    print lastval
  firstdate = firstval.split('T')[0]
  firsttime = firstval.split('T')[1].split('Z')[0]
  lastdate = lastval.split('T')[0]
  lasttime = lastval.split('T')[1].split('Z')[0]
  timediff = diff_times_in_seconds(firsttime,lasttime,firstdate,lastdate)
  print timediff
  #self.timelist.append(timediff)    

filein = './dialogs/10/1.tsv'
with open(filein,'r') as c1:
  c2 = c1.read().split('\n')
makeTimeList(c2)
print checkValidity(c2,0.2,'a')
"""