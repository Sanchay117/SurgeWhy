"""End-to-end tests for SurgeWhy's Track 2 causal proof chain, counterfactual flips & abstention gate."""

from __future__ import annotations

import unittest

from agent.config import ROOT_DIR, load_config
from agent.orchestrator import SurgeWhyOrchestrator


class TestExplainableAdjudicationLoop(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = load_config()
        self.orch = SurgeWhyOrchestrator(self.cfg)

    def test_01_case_01_critic_rejection_and_overturn_proof(self) -> None:
        trace = self.orch.adjudicate_case_file(ROOT_DIR / "input_examples" / "case_01.json")
        self.assertEqual(trace["verdict_code"], "OVERTURNED_PAY_FULL")
        self.assertEqual(trace["total_owed_usd"], 890)
        # Verify non-linear Critic rejection forced Round 2 SQL
        critic_challenges = trace["engines_telemetry"]["world_model"]["critic_challenges"]
        self.assertEqual(len(critic_challenges), 1)
        self.assertEqual(critic_challenges[0]["verdict"], "REVISION_REQUIRED")
        self.assertEqual(len(trace["zetaris_queries"]), 5)
        self.assertEqual(len(trace["nightshift_receipts"]), 6)

    def test_02_counterfactual_simulator_flips_verdict_and_tiers(self) -> None:
        # Baseline CLM-9041: 265m controllable, no ground stop -> $890 ($650 + $240)
        base = self.orch.simulate_counterfactual("CLM-9041", 265, 0, 265, 0)
        self.assertEqual(base["total_payout_usd"], 890)

        # Counterfactual 1: 210m arrival delay -> drops to 50% UK261 tier ($325 + $240 = $565)
        half = self.orch.simulate_counterfactual("CLM-9041", 210, 0, 210, 0)
        self.assertEqual(half["total_payout_usd"], 565)

        # Counterfactual 2: Active FAA Ground Stop -> $0 delay cash, $240 Art. 9 care still owed!
        storm = self.orch.simulate_counterfactual("CLM-9041", 265, 1, 0, 0)
        self.assertEqual(storm["statutory_cash_usd"], 0)
        self.assertEqual(storm["total_payout_usd"], 240)

    def test_03_calibrated_abstention_on_boundary_uncertainty_case_04(self) -> None:
        trace = self.orch.adjudicate_case_file(ROOT_DIR / "input_examples" / "case_04.json")
        self.assertEqual(trace["verdict_code"], "ABSTAIN_NEEDS_PASSENGER_EVIDENCE")
        self.assertTrue(trace["abstention_triggered"])
        self.assertLess(trace["confidence_score"], 0.75)
        self.assertIn("door-open", trace["missing_evidence_request"])

        # Once passenger supplies door-open proof (uncertainty_min = 0 at 184m), payout unlocks to $325!
        unlocked = self.orch.simulate_counterfactual("CLM-9132", 184, 0, 108, 0)
        self.assertEqual(unlocked["simulated_verdict"], "OVERTURNED_PAY_PASSENGER")
        self.assertEqual(unlocked["total_payout_usd"], 325)


if __name__ == "__main__":
    unittest.main()
