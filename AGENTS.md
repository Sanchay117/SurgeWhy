# AGENTS.md: SurgeWhy Technical Contract & AI Coding Agent Instructions

This file instructs Cursor, Claude Code, Windsurf, and other AI coding agents how to work safely and accurately inside the **SurgeWhy** repository for the **Open Agent Hackathon 2026** (**Track 2: The Agent That Can Explain Why**).

---

## 1. Mission & Track 2 Explainability Standard

**SurgeWhy** is an explainable multi-agent airline delay and dynamic fare-surge compensation adjudicator. When an airline denies a passenger's claim with an opaque excuse code (such as `"Extraordinary Weather"` or `"ATC Sequencing"`), SurgeWhy queries four independent aviation and statutory tables through **Zetaris**, challenges its own initial conclusion with an adversarial **Airline Defense Counsel Critic**, computes exact **counterfactual flip boundaries** (*"What minimum change in minutes, wind speed, or evidence flips this verdict?"*), and calibrates confidence so ambiguous boundary cases escalate for human/document proof instead of guessing.

Every verdict produced by SurgeWhy MUST expose four auditable Track 2 pillars:
1. **Causal Chain with Primary-Key Provenance:** Exact path from statutory rule -> carrier gate claim -> live FAA/NOAA METAR telemetry -> aircraft maintenance/crew duty log (`[schema.table#primary_key]`).
2. **Ruled-Out Hypotheses Ledger:** Every competing defense tested and falsified (or upheld!) with concrete SQL row citations.
3. **Counterfactual Flip Deltas:** Exact mathematical thresholds showing what change in telemetry would flip `OVERTURNED` <-> `DENIED` or change the statutory payout dollar amount.
4. **Calibrated Confidence & Abstention Gate:** When split-cause minutes fall inside the sensor/timestamp uncertainty margin (`confidence < 0.75`), pause adjudication (`NEEDS_EVIDENCE`) and specify the exact single passenger document that resolves the boundary.

---

## 2. Three-Layer Sponsor Technical Contracts

### Layer 01: DATA (Zetaris)
- **Endpoints:** Web UI `http://localhost:3000`, REST SQL `POST http://localhost:8888/api/v1.0/sql-editor/sqls/run` (never port `8889`).
- **Required REST Headers:**
  - `Authorization: Bearer <ZETARIS_API_KEY>`
  - `X-Org-ID: 1`
  - `X-Request-ID: <fresh uuid.uuid4() per call>`
- **Single-Statement Rule:** Send **strictly one complete SQL statement per REST call**. Never batch semicolon-separated statements.
- **Preflight First:** Always run `python3 scripts/preflight.py` (`SELECT 1` and `SHOW LIGHTNING DATABASES`) before creating or modifying Zetaris tables.
- **Offline Reproducibility (`SAMPLE_MODE=true`):** `agent/tools_zetaris.py` mirrors the Zetaris schemas (`zetaris_ops`, `zetaris_rest`, `zetaris_maint`, `zetaris_policy`, `pokeapi`) in an in-memory multi-database SQLite federation over `data/sample/` so judges can run every SQL query and test in under 30 seconds without Docker setup.

### Layer 02: BUILD (Cursor & Meterless Engines)
- **Cursor Workflow:** Guided by `AGENTS.md` and `.cursor/rules/surgewhy.mdc`, paired with the Meterless prompt library (`meterless.ai/engines.html`). Document all sponsor integrations in `README.md` and `metadata.json`.
- **All 4 Meterless Engines Implemented & Tested (`agent/engines/`):**
  1. `Scout Intent` (`agent/engines/scout_intent.py`): Classifies passenger dispute type, estimates payout & ambiguity risk, selects Zetaris tables, and assigns Nightshift Nemotron lanes.
  2. `World Model` (`agent/engines/world_model.py`): Shared versioned Causal Hypothesis & Evidence Graph across collaborating agents with optimistic concurrency control (`expected_version`).
  3. `Markovian` (`agent/engines/markovian.py`): Compresses multi-step forensic and legal reasoning into a bounded `CarryOverProofCapsule` (`<= 400 tokens`), eliminating quadratic prompt growth.
  4. `H-MEM` (`agent/engines/h_mem.py`): 3-tier Hierarchical Memory (`EPISODIC`, `SEMANTIC`, `PRECEDENT`) recalling carrier excuse patterns across sessions and persisting verified adjudications.

### Layer 03: POWER (Meterless Nightshift & NVIDIA Nemotron)
- **Endpoint:** `METERLESS_BASE_URL` (`http://127.0.0.1:8088/v1`) using `METERLESS_RUNTIME_TOKEN` and headers `meterless-app: surgewhy-agent`, `meterless-scope: user`.
- **Credential Hygiene:** Never put an NVIDIA API key in `.env`, source code, or Cursor's IDE model settings. Configure NVIDIA inside **Meterless Nightshift -> Setup -> Providers -> NVIDIA**.
- **Explicit Dual NVIDIA Nemotron Lanes:**
  - **Lane 1 (Fast Worker):** `nvidia/nemotron-3.5-lightning-30b-a3b` (Step 1 Intake & Scope, Step 2 Forensics Round 1 SQL, Step 4 Forensics Round 2 SQL).
  - **Lane 2 (Deep Worker):** `nvidia/nemotron-3.5-super-vl-120b-a12b` (Step 3 Devil's Advocate Airline Counsel Critic, Step 5 Counterfactual & Boundary Engine, Step 6 Explainable Legal Brief Generator).
- **Per-Step Attribution:** Every step must emit a `ModelReceipt` recording `model_handled_by`, `lane`, `provider`, `latency_ms`, and token usage.

---

## 3. Verification Commands

```bash
python3 data/download_data.py
python3 smoke_test.py
python3 -m unittest discover -s tests -v
python3 -m agent.main --all-cases
python3 -m agent.main --serve
```
