"""
memory.py — Conversation memory for the Support Copilot.

Responsibilities:
  • MemoryStore  — persist resolved interactions to conversation_memory.json,
                   deduplicate by SHA-256 hash of (ticket + answer).
  • MemoryRetriever — TF-IDF retrieval over stored interactions, same pattern
                      as PolicyRetriever so the interface is familiar.

Nothing in this module touches RAG, order lookup, gates, or the UI.
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "conversation_memory.json")

# Only surface a past interaction if it clears this similarity bar.
# Below this value the hit is treated as irrelevant and silently ignored.
MIN_MEMORY_SCORE = 0.35

# How many past interactions to surface at most (keeps the context window tight).
MAX_MEMORY_HITS = 2


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _interaction_hash(ticket: str, answer: str) -> str:
    """Stable deduplication key — identical ticket+answer always maps to the same hash."""
    payload = (ticket.strip().lower() + "|" + answer.strip().lower()).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_records() -> list:
    if not os.path.exists(MEMORY_PATH):
        return []
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save_records(records: list) -> None:
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# MemoryStore
# ─────────────────────────────────────────────────────────────────────────────

class MemoryStore:
    """Append-only store for resolved interactions with deduplication."""

    def save(self, ticket: str, answer: str, order_id: str = None,
             resolution: str = "auto_resolved") -> bool:
        """
        Persist one interaction.

        Returns True  if the record was newly written.
        Returns False if an identical interaction already exists (duplicate skipped).
        """
        h = _interaction_hash(ticket, answer)
        records = _load_records()

        existing_hashes = {r.get("hash") for r in records}
        if h in existing_hashes:
            return False  # duplicate — skip silently

        record = {
            "hash":       h,
            "timestamp":  datetime.now(timezone.utc).isoformat(),
            "resolution": resolution,
            "order_id":   order_id,
            "ticket":     ticket.strip(),
            "answer":     answer.strip(),
            # The retrieval index uses this combined field as its document.
            # Weighting the ticket twice gives intent more influence than the answer.
            "document":   ticket.strip() + " " + ticket.strip() + " " + answer.strip(),
        }
        records.append(record)
        _save_records(records)
        return True


# ─────────────────────────────────────────────────────────────────────────────
# MemoryRetriever
# ─────────────────────────────────────────────────────────────────────────────

class MemoryRetriever:
    """
    TF-IDF retriever over stored interactions.

    Re-built on each call to ensure newly saved interactions are always
    available without requiring a server restart.
    """

    def retrieve(self, query: str, k: int = MAX_MEMORY_HITS) -> list:
        """
        Return up to k relevant past interactions for the given query.

        Each result dict:
            {
              "ticket":     str,   # original customer message
              "answer":     str,   # agent response
              "order_id":   str|None,
              "timestamp":  str,
              "score":      float,
            }

        Returns an empty list when no history exists or nothing clears the
        MIN_MEMORY_SCORE threshold — caller behaviour is unchanged.
        """
        records = _load_records()
        if len(records) < 2:
            # With only one record, TF-IDF has no IDF discrimination — every
            # query scores the same document at a non-trivial value regardless
            # of relevance. Require at least 2 records before retrieval is useful.
            return []

        documents = [r["document"] for r in records]

        # Need at least 1 document and the query must not be empty
        if not query.strip():
            return []

        try:
            vectorizer = TfidfVectorizer(min_df=1)
            matrix     = vectorizer.fit_transform(documents)
            q_vec      = vectorizer.transform([query])
            sims       = cosine_similarity(q_vec, matrix).flatten()
        except ValueError:
            # Corpus too small (e.g. all stopwords) — return nothing gracefully
            return []

        # Sort descending, take top-k above threshold
        ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in ranked[:k]:
            if score < MIN_MEMORY_SCORE:
                break
            r = records[idx]
            results.append({
                "ticket":    r["ticket"],
                "answer":    r["answer"],
                "order_id":  r.get("order_id"),
                "timestamp": r.get("timestamp", ""),
                "score":     float(score),
            })

        return results
