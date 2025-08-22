"""Summarization utilities.
Replace stub with transformer-based summarizer (e.g., Hugging Face pipeline) later.
"""

from typing import List


def summarize_texts(texts: List[str], max_chars: int = 500) -> str:
	"""Naive stub: concatenates and truncates to max_chars. Replace with LLM."""
	joined = " \n".join(t for t in texts if t)
	return (joined[:max_chars] + ("..." if len(joined) > max_chars else "")) or ""
