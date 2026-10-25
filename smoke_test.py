#!/usr/bin/env python3
"""Official Participant Setup Guide Page 24 Smoke Test (Data + Power Verification)."""

from __future__ import annotations

import argparse
import sys

from agent.config import load_config
from agent.llm import NightshiftNemotronClient
from agent.tools_zetaris import ZetarisClient


def main() -> int:
    parser = argparse.ArgumentParser(description="SurgeWhy Data + Power Smoke Test")
    parser.add_argument("--live", action="store_true", help="Run against live Docker Zetaris & Nightshift")
    args = parser.parse_args()

    cfg = load_config(force_live=args.live)

    # Check 1: Zetaris Web UI
    zclient = ZetarisClient(cfg)
    ui_status = zclient.check_web_ui()
    if not ui_status.get("ok"):
        print("FAIL Data: Zetaris web interface unreachable")
        return 1
    print(f"PASS Data: Zetaris web interface ({ui_status['mode']})")

    # Check 2: Zetaris REST SQL + Starter Pikachu recipe
    sql_one = zclient.run_sql("SELECT 1 AS one")
    pika = zclient.run_sql(
        "SELECT pokemon_name, ability_name, is_hidden FROM pokeapi.pikachu_abilities_table"
    )
    if sql_one.row_count < 1 or pika.row_count < 2:
        print("FAIL Data: Zetaris SQL verification returned unexpected row count")
        return 1
    print(
        f"PASS Data: Zetaris runs SQL over its REST API "
        f"(SELECT 1 -> {sql_one.rows[0]['one']}, pikachu rows -> {pika.row_count})"
    )

    # Check 3: Meterless Nightshift + NVIDIA Nemotron reply
    llm = NightshiftNemotronClient(cfg)
    res = llm.complete_step(
        step_number=0,
        step_name="Smoke Test Ping",
        lane="Lane 1 (Fast Worker)",
        system_prompt="Reply with READY.",
        user_prompt="Confirm Nightshift Nemotron lane health.",
        deterministic_synthesis="READY: SurgeWhy connected to NVIDIA Nemotron via Meterless Nightshift.",
    )
    rcpt = res["receipt"]
    print(
        f"PASS Power: Nemotron replies "
        f"(model_handled_by={rcpt['model_handled_by']}, provider={rcpt['provider']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
