#!/usr/bin/env python3
"""Read-only Zetaris & Meterless Nightshift preflight checker (Setup Guide 1.9 & 4.6)."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.config import load_config
from agent.llm import NightshiftNemotronClient
from agent.tools_zetaris import ZetarisClient


def main() -> int:
    cfg = load_config()
    print(f"SurgeWhy Preflight Check (SAMPLE_MODE={cfg.sample_mode})")
    print("-" * 60)

    zclient = ZetarisClient(cfg)
    r1 = zclient.run_sql("SELECT 1 AS one")
    print(f"[1/3] Zetaris SELECT 1 -> rows={r1.rows} (request_id={r1.request_id})")

    r2 = zclient.run_sql("SHOW LIGHTNING DATABASES")
    print(f"[2/3] Zetaris SHOW LIGHTNING DATABASES -> {len(r2.rows)} registered databases")

    llm = NightshiftNemotronClient(cfg)
    models = llm.list_models()
    print(f"[3/3] Meterless Nightshift /v1/models -> {models}")
    print("PREFLIGHT PASS: Ready for explainable claim adjudication.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
