\
from __future__ import annotations
from typing import List, Tuple
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfVectorStore:
    def __init__(self, vectorizer: TfidfVectorizer, matrix):
        self.vectorizer = vectorizer
        self.matrix = matrix

    @classmethod
    def fit_from_chunks(cls, chunks: List[str]) -> "TfidfVectorStore":
        vectorizer = TfidfVectorizer(
            lowercase=True, stop_words="english", max_df=0.9, min_df=1, ngram_range=(1,2)
        )
        matrix = vectorizer.fit_transform(chunks)
        return cls(vectorizer, matrix)

    def top_k(self, query: str, k: int = 5):
        q = self.vectorizer.transform([query])
        sims = cosine_similarity(q, self.matrix).flatten()
        idxs = sims.argsort()[::-1][:k]
        scores = sims[idxs]
        return scores, idxs

    def save(self, path: Path):
        with open(path, "wb") as f:
            pickle.dump({"vectorizer": self.vectorizer, "matrix": self.matrix}, f)

    @classmethod
    def load(cls, path: Path) -> "TfidfVectorStore":
        with open(path, "rb") as f:
            obj = pickle.load(f)
        return cls(obj["vectorizer"], obj["matrix"])
