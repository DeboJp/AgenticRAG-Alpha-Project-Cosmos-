# task_router.py
import json
import chromadb
from chromadb.config import Settings
from embeddings import embed_texts

# Setup-cromadb for vector search.
chroma = chromadb.PersistentClient(path="vectorstore")
collection = chroma.get_or_create_collection("tool_index")

"""
(Initializer)
Load tool descriptions from JSON file, 
embed them, and store in the vector database.
"""
def index_tools(index_path="tools/index.json"):
    with open(index_path, "r") as f:
        tools = json.load(f)

    descriptions = [tool["description"] for tool in tools]
    ids = [tool["name"] for tool in tools]
    embeddings = embed_texts(descriptions)

    # Clear existing collection for re-indexing
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
    collection.add(ids=ids, embeddings=embeddings, documents=descriptions)

"""
Given a task description, return the top-k matching tool names
using vector similarity over tool descriptions.
"""
def match_tools(task, top_k=2):
    task_embedding = embed_texts([task])[0]
    results = collection.query(query_embeddings=[task_embedding], n_results=top_k)
    # return results["distances"][0]
    return results["ids"][0]  # top tool names
