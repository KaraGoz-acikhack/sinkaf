import joblib
import numpy as np
import re
import string
import torch

from transformers import AutoTokenizer, AutoModel, pipeline
from urllib.request import urlopen


class Sinkaf():

    BERT_MAX_SENTENCE_TOKEN_LENGTH = 113
    PUNCTUATION_TABLE = str.maketrans('', '', string.punctuation)

    def __init__(self):
        self.clf = joblib.load(
            urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/clf.joblib?raw=true"))
        self.vectorizer = joblib.load(
            urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/vectorizer.joblib?raw=true"))
        self.clf_nn = joblib.load(
            urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/clf_nn.joblib?raw=true"))
        # Bert modeli icin kullanilacaklar
        print("Tek seferlik BERT kurulumu gerekebilir.")
        self.tokenizer = AutoTokenizer.from_pretrained(
            "dbmdz/bert-base-turkish-128k-uncased")
        self.bert = AutoModel.from_pretrained(
            "dbmdz/bert-base-turkish-128k-uncased")

    def _bert_vectorize(self, texts):
        input_ids = self._tokenize_input(texts)
        return self._sentence_2_vec(input_ids)

    def _bow_vectorize(self, texts):
        return self.vectorizer.transform(
            [Sinkaf.pre_process(s) for s in texts])

    @staticmethod
    def _get_profane_prob(prob):
        return prob[1]

    @staticmethod
    def _predict_prob(clf, sentence_vectors):
        return np.apply_along_axis(
            Sinkaf._get_profane_prob, 1,
            clf.predict_proba(sentence_vectors))

    def _sentence_2_vec(self, input_ids):
        with torch.no_grad():
            last_hidden_states = self.bert(input_ids)
            features = last_hidden_states[0][:, 0, :].numpy()
        return features

    def _tokenize_input(self, texts):
        tokenized = [self.tokenizer.encode(
            s, add_special_tokens=True) for s in texts]
        padded = np.array(
            [s + [0]*(Sinkaf.BERT_MAX_SENTENCE_TOKEN_LENGTH-len(s)) for s in tokenized])
        # pylint: disable=no-member, not-callable
        input_ids = torch.tensor(np.array(padded)).to(torch.int64)
        return input_ids

    @staticmethod
    def remove_user_names(s):
        # pylint: disable=anomalous-backslash-in-string
        return re.sub("@[^\s]+", "", s)

    @staticmethod
    def remove_numbers(s):
        return re.sub("[0-9]", "", s)

    @staticmethod
    def remove_punctuation(s):
        res = [w.translate(Sinkaf.PUNCTUATION_TABLE) for w in s.split()]
        return " ".join(res)

    @staticmethod
    def n_stemmer(s, n):
        if n > 0:
            res = [x[:n] for x in s.split()]
            return " ".join(res)
        raise Exception("n must be a positive integer!")

    @staticmethod
    def pre_process(s, n=5):
        return Sinkaf.n_stemmer(
            Sinkaf.remove_punctuation(
                Sinkaf.remove_numbers(
                    Sinkaf.remove_user_names(s.lower()))), n)

    def tahmin(self, texts):
        return self.clf.predict(self._bow_vectorize(texts))

    def tahmin_nn(self, texts):
        return self.clf_nn.predict(self._bert_vectorize(texts))

    def tahminlik(self, texts):
        sentence_vectors = self._bow_vectorize(texts)
        return Sinkaf._predict_prob(self.clf, sentence_vectors)

    def tahminlik_nn(self, texts):
        sentence_vectors = self._bert_vectorize(texts)
        return Sinkaf._predict_prob(self.clf_nn, sentence_vectors)
