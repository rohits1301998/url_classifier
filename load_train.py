import numpy as np
import re
import sys
from nltk.util import ngrams
import itertools
import pandas as pd
from sklearn import svm
from joblib import dump, load


#np.set_printoptions(threshold=np.inf)
alphanum = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0','1','2','3','4','5','6','7','8','9']
permutations = itertools.product(alphanum, repeat=3)
featuresDict = {}
counter = 0
for perm in permutations:
    featuresDict[(''.join(perm))] = counter
    counter = counter + 1
#print(counter)
dataset = pd.read_csv("malicious-url-detector_dataset.csv")
dataset = dataset.loc[10000:70000]
# print(dataset.shape[0])
# sys.exit()
X = np.zeros([dataset.shape[0], 46656],dtype="int")
Y = np.zeros(dataset.shape[0],dtype="int")
#print(X)

def preprocess_sentences(df):
    index = 0
    for row in df.iterrows():
        try:
            print(row['url'])
        except:
            continue
        index = index + 1
        url = row['url'].strip().replace("https://","")
        url = url.replace("http://","")
        url = re.sub(r'\.[A-Za-z0-9]+/*','',url)
        for gram in generate_ngram(url):
            try:
                X[index][featuresDict[gram]] = X[index][featuresDict[gram]] + 1
            except:
                print(gram,"doesn't exist")
        Y[index] = int(row['label'])


def generate_ngram(sentence):
    
    s = sentence.lower()
    s = ''.join(e for e in s if e.isalnum()) #replace spaces and slashes
    print(s)
    output = list(ngrams(s,3))
    processedList = []
    for tup in output:
        processedList.append((''.join(tup)))
    return processedList



preprocess_sentences(dataset)
clf = load('svm_model.joblib')
clf.partial_fit(X,Y)
dump(clf, 'svm_model.joblib') 