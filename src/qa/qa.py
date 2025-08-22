"""QA utilities (stub).
Replace with dense retrieval + reader or RAG pipeline.
"""

from typing import List, Tuple


def simple_qa(question: str, texts: List[str]) -> Tuple[str, float]:
	"""Return the most relevant sentence by keyword overlap; score is naive."""
	import re
	q_tokens = set(re.findall(r"\w+", question.lower()))
	best_sent, best_score = "", 0.0
	for t in texts:
		for sent in re.split(r"(?<=[.!?])\s+", t):
			s_tokens = set(re.findall(r"\w+", sent.lower()))
			if not s_tokens:
				continue
			overlap = len(q_tokens & s_tokens) / max(1, len(q_tokens))
			if overlap > best_score:
				best_score, best_sent = overlap, sent
	return best_sent.strip(), float(best_score)
