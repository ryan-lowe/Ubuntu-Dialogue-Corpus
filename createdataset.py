import math
from random import randint
from random import shuffle
import time
import os
import csv

def read_random_line(f, chunk_size=128):
    import os
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

def clean_str(c1,include_s):
  c2 = c1.read().split('\n')
  utterlist = []
  for row in c2:
    row = row.split('\t')
    if len("".join(row[3:])) != 0:
      utterlist.append("".join(row[3:]))
  return utterlist

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
            
              
            

class CreateDataset:

  def __init__(self,path):
    self.traindic = {}
    self.valdic = {}
    self.testdic = {}
    self.filelist = []
    self.path = path
    self.folders = [f for f in os.listdir(self.path)]

  def generateResponses(self, num_responses, convo, testpct):
    fakes = []
    i = 0
    while i < len(num_responses):
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
      """
      fakes.append(read_random_line(fakefile).split('\t')[3:]) 
      """
      with open(fakefile,'r') as c1:
        utterlist = clean_str(c1)
        """
        c = c1.read().split('\n')
        c = c[randint(0,len(c)-1)].split('\t')
        c2 = "".join(c[3:])
        c2 = c2.strip()
        """
        c2 = utterlist[randint(0,len(c)-1)].strip()
        if len(c2) > 1:
          fakes.append(c2)
          i += 1
    return fakes

  def createDicts(self, select, testpct, trainfiles = None, valfiles = None, testfiles = None):
    print 'Creating dictionary of training, validation, and test sets'
    if trainfiles == None:
      for folder in self.folders:
        if select == False or int(folder) > 2:
          filepath = self.path + folder
          for f in os.listdir(filepath):
            self.filelist.append([f, folder])
      shuffle(self.filelist)
      for i in xrange(int(len(self.filelist)*(1-2*testpct))):#0.5)):
        self.traindic[self.filelist[i][0]] = self.filelist[i][1]
        self.writeFiles('../trainfiles.csv', [self.filelist[i]], False)
      for i in xrange(int(len(self.filelist)*(1-2*testpct)),int(len(self.filelist)*(1-testpct))): #0.5),int(len(self.filelist)*0.75)):#
        self.valdic[self.filelist[i][0]] = self.filelist[i][1]
        self.writeFiles('../valfiles.csv', [self.filelist[i]], False)
      for i in xrange(int(len(self.filelist)*(1-testpct)),len(self.filelist)): #0.75),len(self.filelist)):#
        self.testdic[self.filelist[i][0]] = self.filelist[i][1]  
        self.writeFiles('../testfiles.csv', [self.filelist[i]], False)
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
    

  def writeFiles(self, filename, data, listbool):
    csvname = self.path + filename
    with open(csvname,'a+') as out:
      csv_out = csv.writer(out)
      for row in data:
        if listbool:
          for col in row:
            csv_out.writerow(col)
        else:
          csv_out.writerow(row)

  def sortFiles(self, max_context_size, num_options_train, num_options_test, testpct, select, filesperprint):        
    self.createDicts(select, testpct)
    print 'Finished dictionaries, making data files'
    firstline = [['Context','Response','Correct']]
    self.writeFiles('../trainset.csv', firstline,False)
    self.writeFiles('../valset.csv', firstline,False)
    self.writeFiles('../testset.csv', firstline,False)    
    trainexamples = 0
    testexamples = 0
    valexamples = 0
    traindata = []
    valdata = []
    testdata = []         
    for folder in self.folders:     
      if select == False or int(folder) > 2:
        print '   Starting ' + folder + ' folder'
        filepath = self.path + folder
        files = [f for f in os.listdir(filepath)]
        k=0
        for convo in files:
          k+=1
          if k%100 == 0:
            print 'Finished ' + str(k) + 'files'
          #if k % 1000 == 0:
          #    break
          filein = filepath + '/' + convo
          with open(filein,'r') as c1:
            utterlist = clean_str(c1)
            """  #for making badfiles.csv          
            c2 = c1.read().split('\n')
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
              self.writeFiles('../badfiles.csv', [[filein]] ,False)   
            """            
            if utterlist[0] != utterlist[1]:
              if convo in self.traindic:
                for i in xrange(2,len(utterlist) - 1):
                  context = utterlist[max(0,i - max_context_size):i]
                  context = ' </s> '.join(context)  
                  response = utterlist[i]
                  fakes = self.generateResponses(num_options_train - 1, convo, testpct)  
                  data = [[context, response, 1]]
                  for fake in fakes:
                    data.append([context, fake, 0])
                  #self.writeFiles('../trainset.csv', data)  
                  traindata.append(data)
              else:
              
              #generate a context window size, following the approximate distribution of the training set
                contextsize = int((max_context_size*10)/randint(max_context_size/2,max_context_size*10)) + 1 + 1 #last +1 for prediction sentence
                if contextsize > len(utterlist):
                  contextsize = len(utterlist)
                for i in xrange(0,int((len(utterlist))/contextsize)):
                  j = i*contextsize
                  context = utterlist[j:j + contextsize - 1]
                  context = ' </s> '.join(context)  
                  response = utterlist[j + contextsize - 1]
                  fakes = self.generateResponses(num_options_test - 1, convo, testpct)  
                  data = [[context, response, 1]]  
                  for fake in fakes:                  
                    data.append([context, fake, 0])              
                  if convo in self.valdic: 
                    #self.writeFiles('../valset.csv', data)
                    valdata.append(data)
                  else: 
                    #self.writeFiles('../testset.csv', data)
                    testdata.append(data)
            if k % filesperprint == 0 or k == len(files):
              #print 'Finished data files, writing data'
              if traindata != []:
                self.writeFiles('../trainset.csv', traindata, True)
              if valdata != []:
                self.writeFiles('../valset.csv', valdata, True)
              if testdata != []:
                self.writeFiles('../testset.csv', testdata, True)
              traindata = []
              valdata = []
              testdata = []

path='.'
data1 = CreateDataset(path+'/dialogs/')
data1.sortFiles(20,2,2,0.1,True, 50)




#data2 = NormalizeData(path+'Research/ubuntu chatbot/dialogs/', path+'Research/ubuntu chatbot/dialogs2/')


