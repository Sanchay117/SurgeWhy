"""CLI entrypoint and HTTP server for SurgeWhy (Track 2: The Agent That Can Explain Why)."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

from agent.config import ROOT_DIR, SurgeWhyConfig, load_config
from agent.orchestrator import SurgeWhyOrchestrator
from agent.tools_zetaris import ZetarisClient, ZetarisSQLGuardrailError


def format_markdown_report(trace: Dict[str, Any]) -> str:
    lines = [
        f"# SurgeWhy Explainable Adjudication Report: {trace['case_id']} ({trace['flight_number']})",
        "",
        f"- **Claim ID:** `{trace['claim_id']}` | **Route:** `{trace['route']}` | **Carrier:** {trace['carrier_name']}",
        f"- **Airline Initial Decision:** `{trace['carrier_denial_notice']}`",
        f"- **SurgeWhy Verdict:** **{trace['verdict_banner']}**",
        f"- **Calibrated Confidence:** `{int(trace['confidence_score'] * 100)}%` | **Abstention Gate:** `{trace['abstention_triggered']}`",
        "",
        "## 1. Plain-English Why",
        trace["plain_english_why"],
        "",
        "## 2. Cited Causal Proof Chain",
    ]
    for item in trace["causal_chain"]:
        lines.append(f"- **{item['node']}:** {item['fact']} (`[{item['citation']}]`)")

    lines.extend(["", "## 3. Hypotheses Tested & Ruled Out"])
    for hyp in trace["ruled_out_hypotheses"]:
        lines.append(
            f"- **{hyp['title']}** -> `{hyp['status']}`: {hyp['explanation']} "
            f"(Refuted by: `{', '.join(hyp['refuting_citations']) or 'N/A'}`)"
        )

    lines.extend(["", "## 4. Counterfactual Flip Thresholds (What Flips This Decision?)"])
    for cf in trace["counterfactuals"]:
        lines.append(
            f"- **{cf['parameter']}** (Actual: `{cf['actual_value']}`) -> Flip at `{cf['flip_threshold']}`: {cf['flipped_outcome']}"
        )

    if trace["abstention_triggered"]:
        lines.extend(
            [
                "",
                "## 5. Missing Evidence Request (Human Verification Gate)",
                f"> {trace['missing_evidence_request']}",
            ]
        )

    lines.extend(
        [
            "",
            "## 6. Meterless Nightshift & NVIDIA Nemotron Model Receipts",
            "| Step | Agent | Lane | Model Handled By | Latency |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
    )
    for rcpt in trace["nightshift_receipts"]:
        lines.append(
            f"| {rcpt['step_number']} | {rcpt['step_name']} | {rcpt['lane']} | `{rcpt['model_handled_by']}` | {rcpt['latency_ms']} ms |"
        )

    lines.extend(["", "## 7. Ready-to-Send Passenger Notice", "```text", trace["demand_letter"], "```", ""])
    return "\n".join(lines)


def run_all_cases(cfg: SurgeWhyConfig) -> List[Dict[str, Any]]:
    orch = SurgeWhyOrchestrator(cfg)
    in_dir = ROOT_DIR / "input_examples"
    out_dir = ROOT_DIR / "output_examples"
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for case_file in sorted(in_dir.glob("case_*.json")):
        trace = orch.adjudicate_case_file(case_file)
        stem = case_file.stem
        (out_dir / f"{stem}_trace.json").write_text(json.dumps(trace, indent=2), encoding="utf-8")
        (out_dir / f"{stem}_report.md").write_text(format_markdown_report(trace), encoding="utf-8")
        results.append(trace)
        print(
            f"[{trace['case_id']}] {trace['flight_number']} ({trace['route']}) -> "
            f"{trace['verdict_banner']} | confidence={int(trace['confidence_score']*100)}% | "
            f"Markovian saved {trace['engines_telemetry']['markovian']['token_reduction_pct']}% tokens"
        )
    return results


def serve_http(cfg: SurgeWhyConfig, port: int) -> None:
    orch = SurgeWhyOrchestrator(cfg)
    cached_cases = {t["case_id"]: t for t in run_all_cases(cfg)}
    metar_raw = (cfg.sample_dir / "faa_metar_atc.json").read_text(encoding="utf-8")

    class SurgeWhyHandler(BaseHTTPRequestHandler):
        def _send_json(self, obj: Any, status: int = 200) -> None:
            data = json.dumps(obj).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _send_file(self, path: pathlib.Path, content_type: str) -> None:
            if not path.exists():
                self.send_error(404, f"Missing asset: {path.name}")
                return
            raw = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, fmt: str, *args: Any) -> None:
            return

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path in ("/", "/index.html"):
                return self._send_file(ROOT_DIR / "web" / "index.html", "text/html; charset=utf-8")
            if parsed.path in ("/deck", "/deck.html"):
                return self._send_file(ROOT_DIR / "docs" / "deck.html", "text/html; charset=utf-8")
            if parsed.path == "/api/cases":
                return self._send_json({"cases": list(cached_cases.values())})
            if parsed.path == "/api/mock-faa-metar":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(metar_raw.encode("utf-8"))
                return
            if parsed.path == "/api/simulate":
                qs = parse_qs(parsed.query)
                claim_id = (qs.get("claim_id") or ["CLM-9041"])[0]
                arr = int((qs.get("arrival_delay_min") or ["265"])[0])
                gs = int((qs.get("faa_ground_stop_active") or ["0"])[0])
                maint = int((qs.get("controllable_maint_min") or ["265"])[0])
                unc = int((qs.get("door_uncertainty_min") or ["0"])[0])
                sim = orch.simulate_counterfactual(claim_id, arr, gs, maint, unc)
                return self._send_json(sim)
            self.send_error(404, "Not found")

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            if parsed.path == "/api/sql":
                zclient = ZetarisClient(cfg)
                try:
                    rcpt = zclient.run_sql(str(body.get("sql", "SELECT 1 AS one")))
                    return self._send_json({"ok": True, "receipt": rcpt.to_dict()})
                except ZetarisSQLGuardrailError as exc:
                    return self._send_json({"ok": False, "error": str(exc)}, status=400)
                except Exception as exc:
                    return self._send_json({"ok": False, "error": str(exc)}, status=400)
            self.send_error(404, "Not found")

    server = ThreadingHTTPServer(("127.0.0.1", port), SurgeWhyHandler)
    print(f"SurgeWhy Explainability Studio running at http://127.0.0.1:{port}")
    print(f"SurgeWhy 8-Slide Pitch Deck running at  http://127.0.0.1:{port}/deck")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(description="SurgeWhy Track 2 Explainable Compensation Adjudicator")
    parser.add_argument("--case", type=str, help="Run a specific case ID (e.g., CASE-01)")
    parser.add_argument("--all-cases", action="store_true", help="Run all 5 benchmark flight dispute cases")
    parser.add_argument("--serve", action="store_true", help="Launch interactive Web UI & Pitch Deck server")
    parser.add_argument("--port", type=int, default=None, help="Override HTTP port (default 8060)")
    parser.add_argument("--live", action="store_true", help="Disable SAMPLE_MODE and connect to live Zetaris + Nightshift")
    args = parser.parse_args()

    cfg = load_config(force_live=args.live)

    if args.serve:
        serve_http(cfg, args.port or cfg.server_port)
        return 0

    if args.case:
        num = args.case.upper().replace("CASE-", "").zfill(2)
        cpath = ROOT_DIR / "input_examples" / f"case_{num}.json"
        if not cpath.exists():
            print(f"Case file not found: {cpath}", file=sys.stderr)
            return 1
        orch = SurgeWhyOrchestrator(cfg)
        trace = orch.adjudicate_case_file(cpath)
        print(format_markdown_report(trace))
        return 0

    run_all_cases(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
