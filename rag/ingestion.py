import json
import os
import sys

# Ensure backend imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.vector_store import vector_store

def ingest_menu():
    menu_path = os.path.join(os.path.dirname(__file__), '../data/menu/menu.json')
    try:
        with open(menu_path, 'r') as f:
            menu_data = json.load(f)
            
        documents = []
        metadatas = []
        ids = []
        
        for item in menu_data:
            # Create a rich text chunk for each menu item
            doc = f"Menu Item: {item.get('name')}. Price: ${item.get('price')}. "
            if item.get('vegetarian'):
                doc += "This item is vegetarian. "
            if item.get('ingredients'):
                doc += f"Ingredients: {', '.join(item['ingredients'])}."
            
            documents.append(doc)
            metadatas.append({"type": "menu", "name": item.get("name")})
            ids.append(f"menu_{item.get('name').replace(' ', '_').lower()}")
            
        if documents:
            vector_store.add_documents(documents, ids, metadatas)
            print(f"Ingested {len(documents)} menu items.")
            
    except FileNotFoundError:
        print(f"Menu file not found at {menu_path}")

def ingest_policies():
    # Example placeholder for ingesting policies
    documents = [
        "Discount Policy: Students get 10% off their total order upon showing a valid student ID.",
        "Allergy Policy: We maintain strict separation for peanuts to avoid cross-contamination."
    ]
    ids = ["policy_discount_1", "policy_allergy_1"]
    metadatas = [{"type": "policy"}, {"type": "policy"}]
    
    vector_store.add_documents(documents, ids, metadatas)
    print(f"Ingested {len(documents)} policies.")

if __name__ == "__main__":
    print("Starting data ingestion into ChromaDB...")
    ingest_menu()
    ingest_policies()
    print("Ingestion complete.")
