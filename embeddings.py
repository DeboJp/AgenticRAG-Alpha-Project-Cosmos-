# embeddings.py
from sentence_transformers import SentenceTransformer, util

# Load sentence-transformer once globally
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

def embed_texts(texts):
    return model.encode(texts).tolist()

# query_embedding = model.encode('How big is London').tolist()
# passage_embedding = model.encode(['London is known for its finacial district', 'London has 9,787,426 inhabitants at the 2011 census',
#                                 'London is known for its finacial district'])

# print("Similarity:", util.dot_score(query_embedding, passage_embedding))
