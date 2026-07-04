from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from services.storage import load_sections

model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
sections_data = []


def build_index():
    global index, sections_data

    sections_data = load_sections()

    if not sections_data:
        return

    texts = []

    for section in sections_data:
        text = (
            section["section_name"] + " " +
            section["jsx_code"]
        )
        texts.append(text)

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))


def search_sections(query):
    global index, sections_data

    if index is None:
        build_index()

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        5
    )

    results = []

    for idx in indices[0]:
        if idx < len(sections_data):
            results.append(sections_data[idx])

    return results