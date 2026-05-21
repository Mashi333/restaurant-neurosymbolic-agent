# We'll use a lightweight open-source embedding model for the MVP.
# Ensure `sentence-transformers` is installed.
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, text):
        # Returns a list of floats
        return self.model.encode(text).tolist()
    
    def embed_batch(self, texts):
        return self.model.encode(texts).tolist()

# Singleton instance
embedder = Embedder()
