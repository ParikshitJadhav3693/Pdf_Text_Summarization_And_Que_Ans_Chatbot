\
from app.store.vector import TfidfVectorStore

def test_vector_store_topk():
    chunks = [
        "The capital of France is Paris. It is known for the Eiffel Tower.",
        "Python is a programming language commonly used for web apps.",
        "FastAPI is a Python framework for building APIs quickly.",
        "The Eiffel Tower is located in Paris, France."
    ]
    store = TfidfVectorStore.fit_from_chunks(chunks)
    scores, idxs = store.top_k("Where is the Eiffel Tower?", k=2)
    assert len(idxs) == 2
    top_texts = [chunks[i] for i in idxs]
    assert any("Eiffel Tower" in t for t in top_texts)
