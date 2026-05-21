from rag.vector_store import vector_store

class Retriever:
    def retrieve_context(self, query, top_k=3):
        """
        Retrieves top K relevant chunks from the vector store based on the query.
        """
        results = vector_store.search(query, top_k=top_k)
        
        context_str = ""
        for i, res in enumerate(results):
            context_str += f"--- Document {i+1} ---\n"
            context_str += f"{res['content']}\n\n"
            
        return context_str, results

# Singleton instance
retriever = Retriever()
