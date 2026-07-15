import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

POLICY_DIR = os.path.join(os.path.dirname(__file__))


class PolicyRetriever:
    def __init__(self):
        self.chunks = []
        self.sources = []
        self._load()
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform(self.chunks)

    def _load(self):
        for path in glob.glob(os.path.join(POLICY_DIR, "*.md")):
            with open(path) as f:
                text = f.read()
            # chunk by markdown headings
            parts = text.split("\n## ")
            for i, part in enumerate(parts):
                if not part.strip():
                    continue
                label = os.path.basename(path)
                self.chunks.append(part.strip())
                self.sources.append(label)

    def retrieve(self, query: str, k: int = 2):
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix).flatten()
        top_idx = sims.argsort()[::-1][:k]
        return [
            {"source": self.sources[i], "text": self.chunks[i], "score": float(sims[i])}
            for i in top_idx
        ]