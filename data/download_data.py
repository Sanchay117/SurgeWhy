#!/usr/bin/env python3
"""Verify curated SurgeWhy aviation & statutory sample datasets (<25 KB total)."""

from __future__ import annotations

import hashlib
import pathlib
import sys

SAMPLE_DIR = pathlib.Path(__file__).resolve().parent / "sample"

REQUIRED_FILES = [
    "flight_disruptions.csv",
    "faa_metar_atc.json",
    "aircraft_crew_logs.csv",
    "passenger_rights_rules.csv",
    "pikachu_abilities.csv",
    "hmem_seed.json",
]


def main() -> int:
    print("SurgeWhy Sample Dataset Verification")
    print("=" * 56)
    total_bytes = 0
    missing = []
    for fname in REQUIRED_FILES:
        fpath = SAMPLE_DIR / fname
        if not fpath.exists():
            missing.append(fname)
            print(f"[MISSING] {fname}")
            continue
        raw = fpath.read_bytes()
        total_bytes += len(raw)
        digest = hashlib.sha256(raw).hexdigest()[:12]
        print(f"[OK] {fname:<28} {len(raw):>6} bytes  sha256:{digest}")

    print("-" * 56)
    print(f"Total bundle size: {total_bytes} bytes ({total_bytes / 1024:.2f} KB)")
    if missing:
        print(f"ERROR: Missing sample files: {', '.join(missing)}")
        return 1
    print("READY: All 6 Zetaris sample datasets & H-MEM seeds verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
