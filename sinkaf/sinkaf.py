import torch
import joblib
import numpy as np
from urllib.request import urlopen
from transformers import AutoTokenizer, AutoModel


class Sinkaf:

    BERT_MAX_SENTENCE_TOKEN_LENGTH = 113

    def __init__(self, model = "linear"):
        
        self.model = model
        
        if (self.model == "linear"):
            self.clf = joblib.load(urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/model_linearSVC.joblib?raw=true"))
        elif(self.model == "BERT"):
            self.clf = joblib.load(urlopen("https://github.com/eonurk/sinkaf/blob/master/sinkaf/data/clf_nn.joblib?raw=true"))
            # Bert modeli icin kullanilacaklar
            print("Tek seferlik BERT kurulumu gerekebilir.\n")
            self.tokenizer = AutoTokenizer.from_pretrained(
                "dbmdz/bert-base-turkish-128k-uncased")
            self.bert = AutoModel.from_pretrained(
                "dbmdz/bert-base-turkish-128k-uncased")

    def _bert_vectorize(self, texts):
        input_ids = self._tokenize_input(texts)
        return self._sentence_2_vec(input_ids)
        
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

    def tahmin(self, texts):
        if (self.model == "linear"):
            return self.clf.predict(texts)
        elif(self.model == "BERT"):
            return self.clf.predict(self._bert_vectorize(texts))

    def tahminlik(self, texts):
        if (self.model == "linear"):
            return Sinkaf._predict_prob(self.clf, texts)
        elif(self.model == "BERT"):
            sentence_vectors = self._bert_vectorize(texts)
            return Sinkaf._predict_prob(self.clf, sentence_vectors)