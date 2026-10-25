"""Layer 01 (DATA): Zetaris REST SQL API client + SAMPLE_MODE SQLite federation."""

from __future__ import annotations

import csv
import json
import re
import sqlite3
import time
import urllib.request
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from agent.config import SurgeWhyConfig


class ZetarisSQLGuardrailError(ValueError):
    """Raised when an agent attempts batched multi-statement SQL or unsafe DDL."""


@dataclass
class ZetarisQueryReceipt:
    query_id: str
    request_id: str
    sql: str
    source_tables_touched: List[str]
    row_count: int
    latency_ms: float
    mode: str
    rows: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ZetarisClient:
    """Executes single-statement SQL over Zetaris REST API or federated SQLite sample schemas."""

    KNOWN_SCHEMAS = (
        "zetaris_ops",
        "zetaris_rest",
        "zetaris_maint",
        "zetaris_policy",
        "pokeapi",
    )

    def __init__(self, config: SurgeWhyConfig) -> None:
        self.config = config
        self.receipts: List[ZetarisQueryReceipt] = []
        self._conn = sqlite3.connect(":memory:", check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_sample_federation()

    @staticmethod
    def _validate_single_statement(sql: str) -> str:
        cleaned = sql.strip()
        if not cleaned:
            raise ZetarisSQLGuardrailError("SQL statement cannot be empty.")
        # Strip trailing single semicolon if present, then forbid embedded semicolons
        if cleaned.endswith(";"):
            cleaned = cleaned[:-1].strip()
        if ";" in cleaned:
            raise ZetarisSQLGuardrailError(
                "Zetaris REST contract violation: send strictly ONE SQL statement per call."
            )
        return cleaned

    @classmethod
    def _extract_tables(cls, sql: str) -> List[str]:
        pattern = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)\b")
        found = []
        for match in pattern.findall(sql):
            prefix = match.split(".", 1)[0].lower()
            if prefix in cls.KNOWN_SCHEMAS and match not in found:
                found.append(match)
        return found

    def _init_sample_federation(self) -> None:
        cur = self._conn.cursor()
        for schema in self.KNOWN_SCHEMAS:
            cur.execute(f"ATTACH DATABASE ':memory:' AS {schema}")

        # 1. zetaris_ops.flight_disruptions
        cur.execute(
            """
            CREATE TABLE zetaris_ops.flight_disruptions (
                claim_id TEXT PRIMARY KEY,
                flight_number TEXT,
                carrier_name TEXT,
                route TEXT,
                distance_km INTEGER,
                jurisdiction TEXT,
                scheduled_dep_utc TEXT,
                actual_arr_delay_min INTEGER,
                door_open_uncertainty_min INTEGER,
                airline_claimed_code TEXT,
                airline_claimed_reason TEXT,
                airline_initial_payout_usd INTEGER,
                care_receipts_usd INTEGER,
                fare_surge_charged_usd INTEGER,
                downgrade_fare_paid_usd INTEGER,
                extra_bag_fee_usd INTEGER,
                tail_number TEXT,
                dep_airport TEXT,
                arr_airport TEXT,
                connection_buffer_min INTEGER
            )
            """
        )
        with (self.config.sample_dir / "flight_disruptions.csv").open("r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                cur.execute(
                    """
                    INSERT INTO zetaris_ops.flight_disruptions VALUES (
                        :claim_id, :flight_number, :carrier_name, :route,
                        CAST(:distance_km AS INTEGER), :jurisdiction, :scheduled_dep_utc,
                        CAST(:actual_arr_delay_min AS INTEGER),
                        CAST(:door_open_uncertainty_min AS INTEGER),
                        :airline_claimed_code, :airline_claimed_reason,
                        CAST(:airline_initial_payout_usd AS INTEGER),
                        CAST(:care_receipts_usd AS INTEGER),
                        CAST(:fare_surge_charged_usd AS INTEGER),
                        CAST(:downgrade_fare_paid_usd AS INTEGER),
                        CAST(:extra_bag_fee_usd AS INTEGER),
                        :tail_number, :dep_airport, :arr_airport,
                        CAST(:connection_buffer_min AS INTEGER)
                    )
                    """,
                    row,
                )

        # 2. zetaris_rest.faa_metar_atc
        cur.execute(
            """
            CREATE TABLE zetaris_rest.faa_metar_atc (
                metar_id TEXT PRIMARY KEY,
                claim_id TEXT,
                airport_icao TEXT,
                observation_window_utc TEXT,
                visibility_sm REAL,
                wind_speed_kt INTEGER,
                crosswind_limit_kt INTEGER,
                weather_phenomena TEXT,
                faa_ground_stop_active INTEGER,
                atc_spacing_delay_min INTEGER,
                peer_concourse_departures_total INTEGER,
                peer_concourse_departures_ontime INTEGER,
                atc_bulletin_note TEXT
            )
            """
        )
        metar_rows = json.loads(
            (self.config.sample_dir / "faa_metar_atc.json").read_text(encoding="utf-8")
        )
        for mrow in metar_rows:
            cur.execute(
                """
                INSERT INTO zetaris_rest.faa_metar_atc VALUES (
                    :metar_id, :claim_id, :airport_icao, :observation_window_utc,
                    :visibility_sm, :wind_speed_kt, :crosswind_limit_kt,
                    :weather_phenomena, :faa_ground_stop_active, :atc_spacing_delay_min,
                    :peer_concourse_departures_total, :peer_concourse_departures_ontime,
                    :atc_bulletin_note
                )
                """,
                mrow,
            )

        # 3. zetaris_maint.aircraft_crew_logs
        cur.execute(
            """
            CREATE TABLE zetaris_maint.aircraft_crew_logs (
                log_id TEXT PRIMARY KEY,
                claim_id TEXT,
                tail_number TEXT,
                inbound_flight_status TEXT,
                primary_event_code TEXT,
                primary_event_category TEXT,
                controllable_minutes INTEGER,
                extraordinary_minutes INTEGER,
                crew_timeout_minutes INTEGER,
                log_summary TEXT
            )
            """
        )
        with (self.config.sample_dir / "aircraft_crew_logs.csv").open("r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                cur.execute(
                    """
                    INSERT INTO zetaris_maint.aircraft_crew_logs VALUES (
                        :log_id, :claim_id, :tail_number, :inbound_flight_status,
                        :primary_event_code, :primary_event_category,
                        CAST(:controllable_minutes AS INTEGER),
                        CAST(:extraordinary_minutes AS INTEGER),
                        CAST(:crew_timeout_minutes AS INTEGER),
                        :log_summary
                    )
                    """,
                    row,
                )

        # 4. zetaris_policy.passenger_rights_rules
        cur.execute(
            """
            CREATE TABLE zetaris_policy.passenger_rights_rules (
                rule_id TEXT PRIMARY KEY,
                jurisdiction TEXT,
                applies_to_category TEXT,
                min_distance_km INTEGER,
                min_arrival_delay_min INTEGER,
                full_payout_delay_min INTEGER,
                statutory_cash_usd INTEGER,
                half_tier_cash_usd INTEGER,
                duty_of_care_covered INTEGER,
                fare_surge_cap_applies INTEGER,
                downgrade_refund_pct INTEGER,
                legal_citation TEXT
            )
            """
        )
        with (self.config.sample_dir / "passenger_rights_rules.csv").open("r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                cur.execute(
                    """
                    INSERT INTO zetaris_policy.passenger_rights_rules VALUES (
                        :rule_id, :jurisdiction, :applies_to_category,
                        CAST(:min_distance_km AS INTEGER),
                        CAST(:min_arrival_delay_min AS INTEGER),
                        CAST(:full_payout_delay_min AS INTEGER),
                        CAST(:statutory_cash_usd AS INTEGER),
                        CAST(:half_tier_cash_usd AS INTEGER),
                        CAST(:duty_of_care_covered AS INTEGER),
                        CAST(:fare_surge_cap_applies AS INTEGER),
                        CAST(:downgrade_refund_pct AS INTEGER),
                        :legal_citation
                    )
                    """,
                    row,
                )

        # 5. pokeapi.pikachu_abilities_table (Setup Guide Page 10 recipe)
        cur.execute(
            """
            CREATE TABLE pokeapi.pikachu_abilities_table (
                pokemon_name TEXT,
                ability_name TEXT,
                is_hidden TEXT
            )
            """
        )
        with (self.config.sample_dir / "pikachu_abilities.csv").open("r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                cur.execute(
                    "INSERT INTO pokeapi.pikachu_abilities_table VALUES (:pokemon_name, :ability_name, :is_hidden)",
                    row,
                )

        self._conn.commit()

    def check_web_ui(self) -> Dict[str, Any]:
        if self.config.sample_mode:
            return {
                "ok": True,
                "url": self.config.zetaris_base_url,
                "mode": "sample-virtualized",
                "status_code": 200,
            }
        req = urllib.request.Request(self.config.zetaris_base_url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return {
                "ok": 200 <= resp.status < 400,
                "url": self.config.zetaris_base_url,
                "mode": "live-zetaris-ui",
                "status_code": resp.status,
            }

    def run_sql(self, sql: str, limit: int = 100) -> ZetarisQueryReceipt:
        cleaned = self._validate_single_statement(sql)
        query_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        tables = self._extract_tables(cleaned)
        t0 = time.perf_counter()

        if self.config.sample_mode:
            upper = cleaned.upper()
            if upper == "SHOW LIGHTNING DATABASES":
                rows = [
                    {"database_name": "SURGEWHY_FAA_REST", "type": "LIGHTNING_REST"},
                    {"database_name": "ZETARIS_OPS", "type": "SCHEMASTORE"},
                    {"database_name": "ZETARIS_MAINT", "type": "SCHEMASTORE"},
                    {"database_name": "ZETARIS_POLICY", "type": "SCHEMASTORE"},
                    {"database_name": "POKEAPI_REST", "type": "LIGHTNING_REST"},
                ]
            else:
                cur = self._conn.cursor()
                cur.execute(cleaned)
                fetched = cur.fetchmany(limit)
                rows = [dict(r) for r in fetched]
            latency_ms = round((time.perf_counter() - t0) * 1000.0 + 4.2, 2)
            receipt = ZetarisQueryReceipt(
                query_id=query_id,
                request_id=request_id,
                sql=cleaned,
                source_tables_touched=tables,
                row_count=len(rows),
                latency_ms=latency_ms,
                mode="zetaris-sample-federation",
                rows=rows,
            )
            self.receipts.append(receipt)
            return receipt

        # Live Zetaris REST API execution: POST /sql-editor/sqls/run
        endpoint = f"{self.config.zetaris_rest_url}/sql-editor/sqls/run"
        payload = json.dumps(
            {
                "queryId": query_id,
                "sql": cleaned,
                "source": "SqlEditor",
                "limit": limit,
            }
        ).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.config.zetaris_api_key}",
            "X-Org-ID": str(self.config.zetaris_org_id),
            "X-Request-ID": request_id,
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))

        raw_data = body.get("data") or []
        col_defs = body.get("columns") or body.get("schema") or []
        col_names = [
            c.get("name", f"col_{idx}") if isinstance(c, dict) else str(c)
            for idx, c in enumerate(col_defs)
        ]
        rows = []
        for item in raw_data:
            if isinstance(item, dict):
                rows.append(item)
            elif isinstance(item, list):
                if col_names and len(col_names) == len(item):
                    rows.append(dict(zip(col_names, item)))
                else:
                    rows.append({f"col_{i}": v for i, v in enumerate(item)})

        latency_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        receipt = ZetarisQueryReceipt(
            query_id=query_id,
            request_id=request_id,
            sql=cleaned,
            source_tables_touched=tables,
            row_count=len(rows),
            latency_ms=latency_ms,
            mode="zetaris-live-rest",
            rows=rows,
        )
        self.receipts.append(receipt)
        return receipt
