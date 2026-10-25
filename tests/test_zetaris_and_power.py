"""Tests for Zetaris single-statement SQL federation (Layer 01) & Nightshift Nemotron (Layer 03)."""

from __future__ import annotations

import unittest

from agent.config import load_config
from agent.llm import NightshiftNemotronClient
from agent.tools_zetaris import ZetarisClient, ZetarisSQLGuardrailError


class TestZetarisAndPower(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = load_config()

    def test_01_zetaris_single_statement_guardrail_and_federated_join(self) -> None:
        z = ZetarisClient(self.cfg)
        with self.assertRaises(ZetarisSQLGuardrailError):
            z.run_sql("SELECT 1; SELECT 2")

        rcpt = z.run_sql(
            "SELECT f.flight_number, w.visibility_sm, m.primary_event_code "
            "FROM zetaris_ops.flight_disruptions f "
            "JOIN zetaris_rest.faa_metar_atc w ON f.claim_id = w.claim_id "
            "JOIN zetaris_maint.aircraft_crew_logs m ON f.claim_id = m.claim_id "
            "WHERE f.claim_id = 'CLM-9041'"
        )
        self.assertEqual(rcpt.row_count, 1)
        self.assertEqual(rcpt.rows[0]["primary_event_code"], "MEL-32-41")
        self.assertEqual(len(rcpt.source_tables_touched), 3)

    def test_02_nightshift_dual_nemotron_lane_receipts(self) -> None:
        llm = NightshiftNemotronClient(self.cfg)
        r_fast = llm.complete_step(1, "Fast Intake", "Lane 1 (Fast Worker)", "sys", "usr", "ok-fast")
        r_deep = llm.complete_step(3, "Deep Critic", "Lane 2 (Deep Worker)", "sys", "usr", "ok-deep")
        self.assertEqual(r_fast["receipt"]["model_handled_by"], "nvidia/nemotron-3.5-lightning-30b-a3b")
        self.assertEqual(r_deep["receipt"]["model_handled_by"], "nvidia/nemotron-3.5-super-vl-120b-a12b")


if __name__ == "__main__":
    unittest.main()
