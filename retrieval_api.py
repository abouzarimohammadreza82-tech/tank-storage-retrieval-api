from fastapi import FastAPI
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer

from pinecone import Pinecone

# =========================
# تنظیمات
# =========================

PINECONE_API_KEY = "pcsk_6XTJiF_Azamvb6rnwqtZQYaabxDvuaYj794YfSEG39LSvbb6ZkL5tcEf9itQNFp7t81QwM"

INDEX_NAME = "tank-storage-db"

TOP_K = 5

# =========================
# FastAPI
# =========================

app = FastAPI()

# =========================
# Pinecone
# =========================

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(INDEX_NAME)

# =========================
# Embedding Model
# =========================

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# =========================
# Request Model
# =========================

class QueryRequest(BaseModel):
    query: str

# =========================
# Endpoint
# =========================

@app.post("/search")

def search_docs(request: QueryRequest):

    query = request.query

    # ساخت embedding سوال

    query_embedding = model.encode(query).tolist()

    # سرچ در Pinecone

    results = index.query(
        vector=query_embedding,
        top_k=TOP_K,
        include_metadata=True
    )

    contexts = []

    for match in results["matches"]:

        metadata = match.get("metadata", {})

        text = metadata.get("text", "")

        if text:
            contexts.append(text)

    return {
        "query": query,
        "contexts": contexts
    }