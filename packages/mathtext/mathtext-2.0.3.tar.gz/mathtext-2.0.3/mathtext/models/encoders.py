# encoders.py
from sentence_transformers import SentenceTransformer
from sklearn.base import TransformerMixin, BaseEstimator


class BERTEncoder(BaseEstimator, TransformerMixin):
    """ Transforms list of texts (strs) into vectors that represent the meaning of the texts """
    def __init__(self, name='all-MiniLM-L6-v2', **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.encoder = SentenceTransformer(self.name)
        # super().__init__(**kwargs)

    def transform(self, X, copy=None):
        X = list(X)
        return self.encoder.encode(X)

    def fit(self, X, y=None, sample_weight=None):
        return self