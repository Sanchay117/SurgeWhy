"""Meterless Scout Intent Engine: classifies passenger disputes, ambiguity risk & Nightshift routing."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class ScoutIntentDecision:
    intent_type: str
    dispute_severity: str
    ambiguity_risk_score: int
    abstention_watch: bool
    required_zetaris_tables: List[str]
    lane_plan: Dict[str, str]
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ScoutIntentEngine:
    """Routes passenger compensation disputes to Zetaris tables and Nemotron lanes."""

    def classify(
        self,
        carrier_denial_notice: str,
        passenger_statement: str,
        fast_model: str = "nvidia/nemotron-3.5-lightning-30b-a3b",
        deep_model: str = "nvidia/nemotron-3.5-super-vl-120b-a12b",
    ) -> ScoutIntentDecision:
        combined = f"{carrier_denial_notice} {passenger_statement}".lower()

        base_tables = [
            "zetaris_ops.flight_disruptions",
            "zetaris_rest.faa_metar_atc",
            "zetaris_policy.passenger_rights_rules",
        ]
        all_tables = base_tables + ["zetaris_maint.aircraft_crew_logs"]

        lane_plan = {
            "step_1_intake": fast_model,
            "step_2_forensics_r1": fast_model,
            "step_3_counsel_critic": deep_model,
            "step_4_forensics_r2": fast_model,
            "step_5_counterfactual_engine": deep_model,
            "step_6_legal_brief": deep_model,
        }

        if "downgrade" in combined or "business" in combined or "atc-swap" in combined:
            return ScoutIntentDecision(
                intent_type="COMMERCIAL_SWAP_DOWNGRADE",
                dispute_severity="HIGH",
                ambiguity_risk_score=18,
                abstention_watch=False,
                required_zetaris_tables=all_tables,
                lane_plan=lane_plan,
                rationale="Detects equipment swap + involuntary cabin downgrade claim; requires tail assignment audit and 75% tariff rule check.",
            )

        if "de-ic" in combined or "door" in combined or "jetbridge" in combined or "wx-deice" in combined:
            return ScoutIntentDecision(
                intent_type="SPLIT_CAUSE_BOUNDARY_CHECK",
                dispute_severity="HIGH",
                ambiguity_risk_score=74,
                abstention_watch=True,
                required_zetaris_tables=all_tables,
                lane_plan=lane_plan,
                rationale="Detects split mechanical/de-icing delay near 180-minute Henning door-open cliff; activates calibrated abstention watch.",
            )

        if "surge" in combined or "fare difference" in combined or "wx-99" in combined or "microburst" in combined:
            return ScoutIntentDecision(
                intent_type="GENUINE_STORM_SURGE_CAP",
                dispute_severity="MEDIUM",
                ambiguity_risk_score=22,
                abstention_watch=False,
                required_zetaris_tables=all_tables,
                lane_plan=lane_plan,
                rationale="Separates genuine severe weather defense on delay cash from unlawful dynamic fare-surge rebooking charge.",
            )

        if "connection" in combined or "layover" in combined or "catering" in combined or "atc-14" in combined:
            return ScoutIntentDecision(
                intent_type="MISSED_CONNECTION_BUT_FOR",
                dispute_severity="HIGH",
                ambiguity_risk_score=26,
                abstention_watch=False,
                required_zetaris_tables=all_tables,
                lane_plan=lane_plan,
                rationale="Detects tight-connection denial blaming ATC; requires counterfactual but-for subtraction of controllable gate hold.",
            )

        return ScoutIntentDecision(
            intent_type="WEATHER_PRETEXT_AUDIT",
            dispute_severity="CRITICAL",
            ambiguity_risk_score=20,
            abstention_watch=False,
            required_zetaris_tables=all_tables,
            lane_plan=lane_plan,
            rationale="Audits hub weather denial code against NOAA METAR peer departures and aircraft MEL / Part 117 crew logs.",
        )
