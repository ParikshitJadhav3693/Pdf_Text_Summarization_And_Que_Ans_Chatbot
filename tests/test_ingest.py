\
from app.services.ingest import split_into_sentences, chunk_sentences
from app.services.summarizer import frequency_summarize

def test_split_and_chunk():
    text = (
        "FastAPI is a modern web framework. It is fast and easy to use! "
        "We are building a PDF chatbot. This sentence should be in another chunk. "
        "Finally, we test the overlap."
    )
    sents = split_into_sentences(text)
    assert len(sents) >= 3
    chunks = chunk_sentences(sents, chunk_size_words=12, overlap_words=3)
    assert len(chunks) >= 2
    assert any("Finally" in c for c in chunks)

def test_frequency_summary():
    text = (
        "This project builds a chatbot. The chatbot can summarize documents. "
        "Summarization is done with a frequency approach. The approach selects important sentences."
    )
    summary = frequency_summarize(text, max_sentences=2)
    assert isinstance(summary, str)
    assert len(summary) > 0
