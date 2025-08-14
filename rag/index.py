import chromadb
from typing import List, Dict
from sentence_transformers import SentenceTransformer

def get_client(persist_dir: str = "vectorstore"):
    return chromadb.PersistentClient(path=persist_dir)

def get_or_create_collection(client, name: str = "podcasts"):
    return client.get_or_create_collection(name)

def build_index(
    chunks: List[Dict],
    collection_name: str = "podcasts",
    persist_dir: str = "vectorstore",
    embed_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
):
    client = get_client(persist_dir)
    col = get_or_create_collection(client, collection_name)
    model = SentenceTransformer(embed_model_name)

    ids, docs, metas = [], [], []
    for i, ch in enumerate(chunks):
        ids.append(f"{ch['episode_id']}__{i}")
        docs.append(ch["text"])
        metas.append({
            "episode_id": ch["episode_id"],
            "start": float(ch["start"]),
            "end": float(ch["end"])
        })

    embeddings = model.encode(docs, convert_to_numpy=True, normalize_embeddings=True)
    col.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings.tolist())
    return True
