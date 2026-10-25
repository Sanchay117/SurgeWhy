"""Conformance tests for all 4 Meterless Engines in SurgeWhy (Layer 02: BUILD)."""

from __future__ import annotations

import pathlib
import tempfile
import unittest

from agent.config import ROOT_DIR
from agent.engines import (
    CausalWorldModel,
    ConcurrencyConflictError,
    HierarchicalMemoryEngine,
    MarkovianProofEngine,
    ScoutIntentEngine,
)


class TestMeterlessEngines(unittest.TestCase):
    def test_01_scout_intent_dispute_routing_and_ambiguity_gate(self) -> None:
        scout = ScoutIntentEngine()
        d1 = scout.classify(
            "CLAIM DENIED: Code WX-88 Extraordinary Weather at Hub",
            "Clear skies at SFO and gates next to us departed on time.",
        )
        self.assertEqual(d1.intent_type, "WEATHER_PRETEXT_AUDIT")
        self.assertFalse(d1.abstention_watch)
        self.assertIn("zetaris_maint.aircraft_crew_logs", d1.required_zetaris_tables)

        d4 = scout.classify(
            "CLAIM DENIED: Code WX-DEICE Frankfurt de-icing queue",
            "Jetbridge cabin door opened right around 3 hours late.",
        )
        self.assertEqual(d4.intent_type, "SPLIT_CAUSE_BOUNDARY_CHECK")
        self.assertTrue(d4.abstention_watch)
        self.assertGreaterEqual(d4.ambiguity_risk_score, 70)

    def test_02_world_model_causal_graph_and_optimistic_locking(self) -> None:
        wm = CausalWorldModel("CLM-9041")
        self.assertEqual(wm.version, 1)
        v2 = wm.add_evidence(
            node_id="EV-1",
            source_table="zetaris_rest.faa_metar_atc",
            primary_key="METAR-KSFO-1018",
            field_summary="10.0 SM visibility",
            supports_side="PASSENGER",
            agent_name="Forensics",
            expected_version=1,
        )
        self.assertEqual(v2, 2)
        with self.assertRaises(ConcurrencyConflictError):
            wm.upsert_hypothesis(
                hypothesis_id="H1",
                title="Stale write",
                status="PROPOSED",
                explanation="Should fail optimistic lock",
                agent_name="StaleAgent",
                expected_version=1,
            )

    def test_03_markovian_proof_capsule_compression(self) -> None:
        mk = MarkovianProofEngine(max_capsule_tokens=380)
        for idx in range(1, 7):
            mk.transition(
                step_index=idx,
                step_name=f"Step {idx}",
                raw_step_transcript=("SQL row payload and statutory text " * 60),
                world_version=idx + 1,
                verified_citations=["zetaris_ops.flight_disruptions#CLM-9041"],
                open_questions=["Verify tail MEL log"],
                active_verdict_draft="OVERTURNED ($890)",
            )
        metrics = mk.summary_metrics()
        self.assertEqual(metrics["steps_compressed"], 6)
        self.assertGreater(metrics["token_reduction_pct"], 75.0)
        for cap in metrics["capsules"]:
            self.assertLessEqual(cap["capsule_tokens"], 380)

    def test_04_hmem_carrier_pretext_precedent_recall(self) -> None:
        seed = ROOT_DIR / "data" / "sample" / "hmem_seed.json"
        with tempfile.TemporaryDirectory() as tmp:
            runtime_path = pathlib.Path(tmp) / "runtime_hmem.json"
            hmem = HierarchicalMemoryEngine(seed_path=seed, runtime_path=runtime_path)
            hits = hmem.recall("United WX-88 KSFO Part 117 UK261", top_k=2)
            self.assertGreaterEqual(len(hits), 1)
            hmem.commit_precedent(
                claim_id="CLM-TEST-99",
                carrier="Test Air",
                verdict="OVERTURNED",
                rule_applied="UK261-ART7-LH",
                summary="Brake sensor fault overturned weather pretext",
                tags=["WX-88", "MEL-32-41"],
            )
            # Re-instantiate from persisted disk file to prove cross-session memory
            hmem2 = HierarchicalMemoryEngine(seed_path=seed, runtime_path=runtime_path)
            hits2 = hmem2.recall("MEL-32-41 Brake sensor", top_k=2)
            self.assertTrue(any(h.get("case_ref") == "CLM-TEST-99" for h in hits2))


if __name__ == "__main__":
    unittest.main()
