import re
import string
import joblib
import numpy as np
import pkg_resources
from urllib.request import urlopen

table = str.maketrans('', '', string.punctuation)
vectorizer = joblib.load(urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/vectorizer.joblib?raw=true"))
model = joblib.load(urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/model.joblib?raw=true"))

def lower(s):
    return s.lower()

def removeUserNames(s):
    return re.sub('@[^\s]+','',s)

def removeNumbers(s):
    return re.sub('[0-9]','',s)

def removePunctuation(s):
    res = [w.translate(table) for w in s.split()]
    return " ".join(res)

def nStemmer(s, n):
    if(n>0):
        res = [x[:n] for x in s.split()]
        return " ".join(res)
    raise Exception("n must be a positive integer!")


def preProcess(s, n=10):
    return nStemmer(removePunctuation(removeNumbers(removeUserNames(lower(s)))),n)


def tahmin(texts):
        return model.predict(vectorizer.transform([preProcess(p) for p in texts]))

def _get_profane_prob(prob):
  return prob[1]

def tahminlik(texts):
    return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform([preProcess(p) for p in texts])))