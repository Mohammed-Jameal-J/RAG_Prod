import os
import time
from collections import deque

import faiss
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Copy .env.example to .env and add your key."
    )

_client = Groq(api_key=GROQ_API_KEY)
_embedder = None

RATE_LIMIT_MAX_REQUESTS = 20
RATE_LIMIT_WINDOW_SECONDS = 60.0
_request_times: deque[float] = deque()

_ANSWER_CACHE_MAX_SIZE = 200
_answer_cache: dict[tuple, str] = {}


def check_rate_limit() -> bool:
    """Shared sliding-window limit across every visitor, protecting the Groq quota.

    Returns True if this request is allowed (and records it), False if the
    app is currently over the limit.
    """
    now = time.time()
    while _request_times and now - _request_times[0] > RATE_LIMIT_WINDOW_SECONDS:
        _request_times.popleft()
    if len(_request_times) >= RATE_LIMIT_MAX_REQUESTS:
        return False
    _request_times.append(now)
    return True


def get_embedder():
    global _embedder
    if _embedder is None:
        from fastembed import TextEmbedding

        _embedder = TextEmbedding()
    return _embedder


def load_pdf(file) -> tuple[str, int]:
    reader = PdfReader(file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text, len(reader.pages)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


class EmbeddingIndex:
    def __init__(self):
        self.index = None
        self.chunks: list[str] = []

    def build(self, chunks: list[str]) -> None:
        embedder = get_embedder()
        vectors = np.asarray(list(embedder.embed(chunks)), dtype="float32")
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)
        self.chunks = chunks

    def search(self, query: str, k: int = 4) -> list[str]:
        if self.index is None or not self.chunks:
            return []
        embedder = get_embedder()
        query_vector = np.asarray(list(embedder.embed([query])), dtype="float32")
        k = min(k, len(self.chunks))
        _, indices = self.index.search(query_vector, k)
        return [self.chunks[i] for i in indices[0] if i != -1]

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)


def ask_groq(question: str, context_chunks: list[str], history: list[dict]):
    # Only cache first-turn questions (no prior conversation) - history makes
    # the same question mean different things depending on what preceded it.
    cache_key = (question.strip().lower(), tuple(context_chunks)) if not history else None
    if cache_key is not None and cache_key in _answer_cache:
        yield _answer_cache[cache_key]
        return

    context = "\n\n---\n\n".join(context_chunks) if context_chunks else "No context available."

    system_prompt = (
        "You are a helpful assistant that answers questions using only the "
        "provided document context. If the answer is not contained in the "
        "context, say you couldn't find it in the document instead of "
        "guessing. Greetings and small talk (e.g. \"hi\", \"thanks\", "
        "\"who are you\") aren't document questions - reply to those "
        "naturally and briefly instead of saying you couldn't find them "
        "in the document.\n\nContext:\n" + context
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": question})

    stream = _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
        stream=True,
    )

    answer_parts = []
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            answer_parts.append(delta)
            yield delta

    if cache_key is not None:
        if len(_answer_cache) >= _ANSWER_CACHE_MAX_SIZE:
            _answer_cache.pop(next(iter(_answer_cache)))
        _answer_cache[cache_key] = "".join(answer_parts)
