from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import numpy as np
import random
import re
from nltk.util import ngrams
import itertools
import pandas as pd
from sklearn import svm
from joblib import dump, load
import os
from django.conf import settings

# Create your views here.

def preprocess_sentences(url):
    alphanum = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0','1','2','3','4','5','6','7','8','9']
    permutations = itertools.product(alphanum, repeat=3)
    featuresDict = {}
    X = np.zeros([1, 46656],dtype="int")
    counter = 0
    for perm in permutations:
        featuresDict[(''.join(perm))] = counter
        counter = counter + 1
    url = url.strip().replace("https://","")
    url = url.replace("http://","")
    url = re.sub(r'\.[A-Za-z0-9]+/*','',url)
    for gram in generate_ngram(url):
        try:
            X[0][featuresDict[gram]] = X[0][featuresDict[gram]] + 1
        except:
            print(gram,"doesn't exist")
    return X
       

def generate_ngram(sentence):
    
    s = sentence.lower()
    s = ''.join(e for e in s if e.isalnum()) #replace spaces and slashes
    print(s)
    output = list(ngrams(s,3))
    processedList = []
    for tup in output:
        processedList.append((''.join(tup)))
    return processedList

def index(request):
    if request.method == "POST":
        X = preprocess_sentences(request.POST.get("url"))
        print(X)
        svm = load(os.path.join(settings.BASE_DIR,'svm_model.joblib'))
        prediction = svm.predict(X)
        print(prediction)
        status = ""
        if prediction[0] == 1:
            status = "Malicious"
        else:
            status = "Safe"
        result = {"status":status}
    if request.method == "GET":
        result = {}
    return render(request,'index.html',result)

