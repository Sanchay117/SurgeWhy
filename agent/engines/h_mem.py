"""Meterless H-MEM Engine: 3-tier persistent memory for airline pretext & legal precedents."""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any, Dict, List


class HierarchicalMemoryEngine:
    """Stores and recalls Episodic, Semantic, and Precedent claim memories across sessions."""

    def __init__(self, seed_path: pathlib.Path, runtime_path: pathlib.Path) -> None:
        self.seed_path = seed_path
        self.runtime_path = runtime_path
        self.store: Dict[str, List[Dict[str, Any]]] = {"episodic": [], "semantic": [], "precedent": []}
        self._load()

    def _load(self) -> None:
        if self.runtime_path.exists():
            self.store = json.loads(self.runtime_path.read_text(encoding="utf-8"))
        elif self.seed_path.exists():
            self.store = json.loads(self.seed_path.read_text(encoding="utf-8"))

    def recall(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        tokens = {
            tok.lower()
            for tok in re.findall(r"[a-zA-Z0-9_-]{2,}", query_text)
        }
        scored = []
        for tier in ("precedent", "semantic", "episodic"):
            for item in self.store.get(tier, []):
                blob = json.dumps(item).lower()
                tags = [str(t).lower() for t in item.get("tags", [])]
                score = sum(3 for t in tags if t in blob and any(q in t or t in q for q in tokens))
                score += sum(1 for q in tokens if len(q) >= 3 and q in blob)
                if score > 0:
                    scored.append((score, tier.upper(), item))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, tier_label, item in scored[:top_k]:
            entry = dict(item)
            entry["tier"] = tier_label
            entry["relevance_score"] = score
            results.append(entry)
        return results

    def commit_precedent(
        self,
        claim_id: str,
        carrier: str,
        verdict: str,
        rule_applied: str,
        summary: str,
        tags: List[str],
    ) -> Dict[str, Any]:
        next_idx = len(self.store.get("precedent", [])) + 301
        record = {
            "memory_id": f"HMEM-PREC-{next_idx}",
            "case_ref": claim_id,
            "carrier": carrier,
            "verdict": verdict,
            "rule_applied": rule_applied,
            "summary": summary,
            "tags": tags,
        }
        # Replace if claim_id already exists to keep idempotent runs clean
        existing = [p for p in self.store.get("precedent", []) if p.get("case_ref") != claim_id]
        existing.append(record)
        self.store["precedent"] = existing
        self.runtime_path.parent.mkdir(parents=True, exist_ok=True)
        self.runtime_path.write_text(json.dumps(self.store, indent=2), encoding="utf-8")
        return record
