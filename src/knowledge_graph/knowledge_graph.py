"""Knowledge graph construction (stub).
Uses simple noun-like token co-occurrence to form edges. Replace with NER/RE later.
"""

from typing import List, Dict, Any


def build_concept_graph(texts: List[str]) -> Dict[str, Any]:
	try:
		import networkx as nx
	except Exception:
		raise RuntimeError("networkx is required for knowledge graph creation.")

	import re
	G = nx.Graph()
	for t in texts:
		# naive 'entities' = unique TitleCase words or capitalized tokens
		tokens = re.findall(r"\b[A-Z][a-zA-Z0-9_\-]+\b", t)
		uniq = list(dict.fromkeys(tokens))
		for node in uniq:
			G.add_node(node)
		for i in range(len(uniq) - 1):
			a, b = uniq[i], uniq[i + 1]
			if a != b:
				G.add_edge(a, b, weight=1)

	# Return a portable representation
	return {
		"nodes": [{"id": n, **G.nodes[n]} for n in G.nodes()],
		"edges": [{"source": u, "target": v, **d} for u, v, d in G.edges(data=True)],
	}
