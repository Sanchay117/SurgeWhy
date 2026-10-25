"""Meterless Markovian Thinking Engine: bounded CarryOverProofCapsule compression across steps."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class CarryOverProofCapsule:
    step_index: int
    step_name: str
    world_version: int
    verified_citations: List[str]
    open_questions: List[str]
    active_verdict_draft: str
    capsule_tokens: int
    raw_cumulative_tokens: int


class MarkovianProofEngine:
    """Maintains flat O(1) bounded prompt context across multi-step forensic adjudication."""

    def __init__(self, max_capsule_tokens: int = 380) -> None:
        self.max_capsule_tokens = max_capsule_tokens
        self.capsules: List[CarryOverProofCapsule] = []
        self._raw_running_tokens: int = 0

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, int(len(text) / 3.8))

    def transition(
        self,
        step_index: int,
        step_name: str,
        raw_step_transcript: str,
        world_version: int,
        verified_citations: List[str],
        open_questions: List[str],
        active_verdict_draft: str,
    ) -> CarryOverProofCapsule:
        step_raw_tokens = self.estimate_tokens(raw_step_transcript)
        # In naive history accumulation, every subsequent turn re-sends all prior raw turns
        prior_raw = self.capsules[-1].raw_cumulative_tokens if self.capsules else 0
        self._raw_running_tokens += step_raw_tokens
        naive_cumulative = prior_raw + self._raw_running_tokens

        compact_payload = {
            "step": step_index,
            "v": world_version,
            "citations": verified_citations[:8],
            "open": open_questions[:3],
            "draft": active_verdict_draft[:220],
        }
        serialized = json.dumps(compact_payload, separators=(",", ":"))
        capsule_tokens = min(self.max_capsule_tokens, self.estimate_tokens(serialized) + 42)

        capsule = CarryOverProofCapsule(
            step_index=step_index,
            step_name=step_name,
            world_version=world_version,
            verified_citations=list(verified_citations[:8]),
            open_questions=list(open_questions[:3]),
            active_verdict_draft=active_verdict_draft[:220],
            capsule_tokens=capsule_tokens,
            raw_cumulative_tokens=naive_cumulative,
        )
        self.capsules.append(capsule)
        return capsule

    def summary_metrics(self) -> Dict[str, Any]:
        if not self.capsules:
            return {
                "steps_compressed": 0,
                "naive_cumulative_tokens": 0,
                "markovian_total_tokens": 0,
                "token_reduction_pct": 0.0,
                "max_capsule_budget": self.max_capsule_tokens,
                "capsules": [],
            }
        naive_total = self.capsules[-1].raw_cumulative_tokens
        markov_total = sum(c.capsule_tokens for c in self.capsules)
        reduction = round((1.0 - (markov_total / max(1, naive_total))) * 100.0, 1)
        return {
            "steps_compressed": len(self.capsules),
            "naive_cumulative_tokens": naive_total,
            "markovian_total_tokens": markov_total,
            "token_reduction_pct": reduction,
            "max_capsule_budget": self.max_capsule_tokens,
            "capsules": [asdict(c) for c in self.capsules],
        }
