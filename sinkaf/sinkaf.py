import joblib
import numpy as np
import pkg_resources
import re
import string

from urllib.request import urlopen

table = str.maketrans('', '', string.punctuation)
vectorizer = joblib.load(
    urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/vectorizer.joblib?raw=true"))
clf = joblib.load(
    urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/clf.joblib?raw=true"))


def remove_user_names(s):
    return re.sub("@[^\s]+", "", s)


def remove_numbers(s):
    return re.sub("[0-9]", "", s)


def remove_punctuation(s):
    res = [w.translate(table) for w in s.split()]
    return " ".join(res)


def n_stemmer(s, n):
    if n > 0:
        res = [x[:n] for x in s.split()]
        return " ".join(res)
    raise Exception("n must be a positive integer!")


def pre_process(s, n=5):
    return n_stemmer(remove_punctuation(remove_numbers(remove_user_names(s))), n)


def tahmin(texts):
    return clf.predict(
        vectorizer.transform([pre_process(sentence) for sentence in texts])
    )


def _get_profane_prob(prob):
    return prob[1]


def tahminlik(texts):
    return np.apply_along_axis(
        _get_profane_prob, 1,
        clf.predict_proba(
            vectorizer.transform([pre_process(s) for s in texts])))
