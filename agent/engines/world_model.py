"""Meterless World Model Engine: versioned causal proof graph, hypothesis ledger & optimistic locking."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


class ConcurrencyConflictError(RuntimeError):
    """Raised when an agent attempts a stale write against CausalWorldModel."""


@dataclass
class EvidenceNode:
    node_id: str
    source_table: str
    primary_key: str
    field_summary: str
    supports_side: str  # PASSENGER, AIRLINE, or BOUNDARY_WARNING
    recorded_by: str
    world_version: int


@dataclass
class CausalHypothesis:
    hypothesis_id: str
    title: str
    proposed_by: str
    status: str  # PROPOSED, CHALLENGED_BY_COUNSEL, FALSIFIED, UPHELD_AIRLINE, VERIFIED_ROOT_CAUSE, AMBIGUOUS_BOUNDARY
    supporting_citations: List[str] = field(default_factory=list)
    refuting_citations: List[str] = field(default_factory=list)
    explanation: str = ""


class CausalWorldModel:
    """Shared state graph for multi-agent causal proofs, ruled-out defenses & counterfactuals."""

    def __init__(self, claim_id: str) -> None:
        self.claim_id = claim_id
        self.version: int = 1
        self.evidence_nodes: Dict[str, EvidenceNode] = {}
        self.hypotheses: Dict[str, CausalHypothesis] = {}
        self.critic_challenges: List[Dict[str, Any]] = []
        self.counterfactual_deltas: List[Dict[str, Any]] = []
        self.history: List[Dict[str, Any]] = [
            {"version": 1, "agent": "system", "event": f"Initialized CausalWorldModel for {claim_id}"}
        ]

    def _check_and_bump(self, expected_version: Optional[int], agent_name: str, action: str) -> int:
        if expected_version is not None and expected_version != self.version:
            raise ConcurrencyConflictError(
                f"Version mismatch for {agent_name}: expected v{expected_version}, actual v{self.version}."
            )
        self.version += 1
        self.history.append({"version": self.version, "agent": agent_name, "event": action})
        return self.version

    def add_evidence(
        self,
        node_id: str,
        source_table: str,
        primary_key: str,
        field_summary: str,
        supports_side: str,
        agent_name: str,
        expected_version: Optional[int] = None,
    ) -> int:
        ver = self._check_and_bump(expected_version, agent_name, f"Added evidence {node_id} from {source_table}#{primary_key}")
        self.evidence_nodes[node_id] = EvidenceNode(
            node_id=node_id,
            source_table=source_table,
            primary_key=primary_key,
            field_summary=field_summary,
            supports_side=supports_side,
            recorded_by=agent_name,
            world_version=ver,
        )
        return ver

    def upsert_hypothesis(
        self,
        hypothesis_id: str,
        title: str,
        status: str,
        explanation: str,
        agent_name: str,
        supporting_citations: Optional[List[str]] = None,
        refuting_citations: Optional[List[str]] = None,
        expected_version: Optional[int] = None,
    ) -> int:
        ver = self._check_and_bump(expected_version, agent_name, f"Hypothesis {hypothesis_id} -> {status}")
        existing = self.hypotheses.get(hypothesis_id)
        sup = list(supporting_citations or (existing.supporting_citations if existing else []))
        ref = list(refuting_citations or (existing.refuting_citations if existing else []))
        self.hypotheses[hypothesis_id] = CausalHypothesis(
            hypothesis_id=hypothesis_id,
            title=title or (existing.title if existing else hypothesis_id),
            proposed_by=existing.proposed_by if existing else agent_name,
            status=status,
            supporting_citations=sup,
            refuting_citations=ref,
            explanation=explanation,
        )
        return ver

    def record_critic_challenge(
        self,
        challenge_id: str,
        verdict: str,
        objection: str,
        required_sql_followup: str,
        agent_name: str,
        expected_version: Optional[int] = None,
    ) -> int:
        ver = self._check_and_bump(expected_version, agent_name, f"Critic challenge {challenge_id}: {verdict}")
        self.critic_challenges.append(
            {
                "challenge_id": challenge_id,
                "verdict": verdict,
                "objection": objection,
                "required_sql_followup": required_sql_followup,
                "world_version": ver,
            }
        )
        return ver

    def set_counterfactuals(
        self,
        deltas: List[Dict[str, Any]],
        agent_name: str,
        expected_version: Optional[int] = None,
    ) -> int:
        ver = self._check_and_bump(expected_version, agent_name, f"Recorded {len(deltas)} counterfactual flip rules")
        self.counterfactual_deltas = deltas
        return ver

    def snapshot(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "version": self.version,
            "evidence_nodes": {k: asdict(v) for k, v in self.evidence_nodes.items()},
            "hypotheses": {k: asdict(v) for k, v in self.hypotheses.items()},
            "critic_challenges": list(self.critic_challenges),
            "counterfactual_deltas": list(self.counterfactual_deltas),
            "history": list(self.history),
        }
