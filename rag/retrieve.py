from typing import List, Tuple
from sentence_transformers import SentenceTransformer
def retrieve(...):
    import chromadb
    from chromadb.config import Settings

    client = chromadb.Client(Settings(
        persist_directory=None
    ))
    # rest of your retrieval code...

def get_collection(persist_dir: str = "vectorstore", collection_name: str = "podcasts"):
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_collection(collection_name)

def retrieve(
    query: str,
    k: int = 8,
    persist_dir: str = "vectorstore",
    collection_name: str = "podcasts",
    embed_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
) -> List[Tuple[str, str, dict]]:
    model = SentenceTransformer(embed_model_name)
    col = get_collection(persist_dir, collection_name)

    q_emb = model.encode([query], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=q_emb, n_results=k)

    hits = []
    for _id, doc, meta in zip(res["ids"][0], res["documents"][0], res["metadatas"][0]):
        hits.append((_id, doc, meta))
    return hits
