import os
import chromadb
from rag.embeddings import embedder

DB_PATH = os.path.join(os.path.dirname(__file__), "vectordb", "chroma_db")

class VectorStore:
    def __init__(self):
        # Initialize ChromaDB persistent client
        self.client = chromadb.PersistentClient(path=DB_PATH)
        # We create a single collection for MVP. Later we can separate menu and policies.
        self.collection = self.client.get_or_create_collection(
            name="restaurant_knowledge"
        )
        
    def add_documents(self, documents, ids, metadatas=None):
        """
        documents: list of text strings
        ids: list of unique string IDs
        metadatas: list of metadata dicts
        """
        embeddings = embedder.embed_batch(documents)
        self.collection.upsert(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas or [{} for _ in documents]
        )
        
    def search(self, query, top_k=3):
        query_embedding = embedder.embed_text(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results for easy usage
        formatted_results = []
        if results and "documents" in results and results["documents"]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if "metadatas" in results else {},
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
        return formatted_results

# Singleton instance
vector_store = VectorStore()
