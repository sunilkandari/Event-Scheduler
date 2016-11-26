import numpy as np
import re
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import pandas as pd
# fix random seed for reproducibility
np.random.seed(7)


#######################################################################################
print "Load training dataset"
X_train, y_train = [], []
f = open("./PreProcess/preprocessed_filtered.txt")
for l in f:
    if l.count(" ") == 0 :
        continue;
    key, val = l.split()
    key = re.sub('[^0-9a-zA-Z]+', '', key)
    if len(key.strip())==0:
        continue;
    X_train += [ key.lower().strip() ]
    y_train += [ val ]


d = {}
f = open("./Word_Embeedings/Text_filtered.vectors.txt")
for l in f:
    words = l.split()
    d[ str(words[0]).strip() ] = [ float(v) for v in words[1:] ]


found = 0
notFound = []
newX = []
newY = []
for i in xrange( len(X_train) ):
    key = str(X_train[i]).strip()
    key = key.lower();
    if key in d:
        newX += [ d[key] ]
        newY += [ 0 if y_train[i].strip() == 'none' else 1]
        found += 1
    else:
        notFound += [key]
print "Number of words for training: ", found, " out of ", len(X_train)



newX = np.array( [ np.array(x) for x in newX ] )
newY = np.array( [ np.array(x) for x in newY ] )
print newX.shape, newY.shape


def create_dataset( wordsList, datasetX, datasetY, window=5):
    dataX, dataY = [], []
    targetWords = []
    for i in range(len(datasetX)-window):
        dataX.append(datasetX[i:(i+window)])
        dataY.append(datasetY[i + window/2])
        if wordsList is not None:
        	targetWords += [ wordsList[i+window/2] ]
    return np.array(dataX), np.array(dataY), targetWords

trainX, trainY,x = create_dataset( None, newX, newY, 5 )


#######################################################################################
print "Building Model..."
model = Sequential()
model.add( LSTM(32, input_dim=10) )
model.add(Dropout(0.3))
model.add( Dense(1) )
model.compile( loss="mean_squared_error", optimizer="adam", metrics=['accuracy'] )
model.fit( trainX, trainY, nb_epoch=100, batch_size=10 )


trainScore = model.evaluate(trainX, trainY, batch_size=1, verbose=0 )
print "trainScore: ", trainScore


#######################################################################################
print "Load test dataset"
x_test, y_test = [], []
f = open("./PreProcess/test_preprocessed.txt")
for l in f:
    if l.count(" ") == 0 :
        continue;
    l = l.split()
    key, val = l[0], l[1]
    key = re.sub('[^0-9a-zA-Z]+', '', key)
    if len(key.strip())==0:
        continue;
    x_test += [ key.lower().strip() ]
    y_test += [ val ]


found = 0
notFound = []
testX = []
testY = []
testWords = []
for i in xrange( len(x_test) ):
    key = str(x_test[i]).strip()
    key = key.lower();
    if key in d:    	
    	testWords += [ key ]
        testX += [ d[key] ]
        testY += [ 0 if y_test[i].strip() == 'none' else 1]
        found += 1
    else:
        notFound += [key]
print "Number of words for Testing: ", found, " out of ", len(testX)


newX = np.array( [ np.array(x) for x in testX ] )
newY = np.array( [ np.array(x) for x in testY ] )
print newX.shape, newY.shape

testX, testY, words = create_dataset( testWords, newX, newY, 5 )


#######################################################################################
print "Evaluating the model"
predictions = model.predict(testX)
predictions = [ 1 if i>=0.5 else 0 for i in predictions ]
predOnes = 0
for i in xrange(len(predictions)):
    predOnes += (1 if predictions[i]==1 else 0 )    
groundOnes = 0
for i in xrange(len(testY)):
    groundOnes += (1 if testY[i]==1 else 0 )    
correctPredicOnes = 0
for i in xrange(len(predictions)):
    correctPredicOnes += (1 if predictions[i]==testY[i] else 0 )    
print predOnes, groundOnes, correctPredicOnes


p = 1.0*correctPredicOnes / predOnes
r = 1.0*correctPredicOnes / groundOnes
print "Precision: ", p
print "Recall: ", r
print "F-Score: ", 2 * p* r/ (p+r)


print "Writing Predicted Named Entities to EntitiesYes.lst"
print "Writing Predicted Multiword Named Entities to NERPhrases.lst"
print "Writing Predicted NON Named Entities to EntitiesNo.lst"
fYes = open("EntitiesYes.lst", "w+")
fNo = open("EntitiesNo.lst", "w+")
fPhrases = open("EntitiesMultiWord.lst", "w+")
s = ""
for i in xrange(len(predictions)):
    if predictions[i] == 1:
        fYes.write( words[i] +"\n")
        s += (words[i] + " ")
    else:
        if len(s) != 0:
            fPhrases.write( s +"\n")
        s = ""
        fNo.write( words[i] +"\n")
fYes.close()
fNo.close()
fPhrases.close()