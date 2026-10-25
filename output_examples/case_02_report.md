# SurgeWhy Explainable Adjudication Report: CASE-02 (BA-112)

- **Claim ID:** `CLM-9088` | **Route:** `JFK -> LHR -> CDG` | **Carrier:** British Airways
- **Airline Initial Decision:** `CLAIM DENIED ($0 PAYOUT): Missed Heathrow connection to Paris caused by Air Traffic Control sequencing at JFK (Code ATC-14).`
- **SurgeWhy Verdict:** **OVERTURNED: PAY $715 ($650 EU261/UK261 + $65 Meal Care)**
- **Calibrated Confidence:** `95%` | **Abstention Gate:** `False`

## 1. Plain-English Why
British Airways blamed JFK Air Traffic Control (Code ATC-14) for missing your Heathrow->Paris connection, but FAA logs show ATC delayed departure by only 14 minutes out of your 77-minute connection buffer. Gate log OPS-CAT-19 reveals BA held the plane 41 minutes for late catering carts and gate staffing; without BA's 41-minute catering delay, you would have landed with 63 minutes to spare (18 minutes above the 45-minute connection minimum) and made your Paris flight.

## 2. Cited Causal Proof Chain
- **1. Airline Claim:** Carrier blamed JFK ATC sequencing (ATC-14) for missed LHR connection ($0 paid) (`[zetaris_ops.flight_disruptions#CLM-9088]`)
- **2. ATC Share Quantified:** KJFK ocean-track spacing added only 14m (leaving 63m of passenger's 77m layover) (`[zetaris_rest.faa_metar_atc#METAR-KJFK-1019]`)
- **3. But-For Cause Proven:** Tail G-XWBA held 41m for late catering & gate staffing (63m - 41m = 22m < 45m MCT -> missed flight) (`[zetaris_maint.aircraft_crew_logs#OPS-CAT-19]`)
- **4. Final Arrival Rule:** 248m final Paris arrival delay >= 240m under Folkerts (C-11/11) = $650 + $65 = $715 (`[zetaris_policy.passenger_rights_rules#EU261-ART7-CONN]`)

## 3. Hypotheses Tested & Ruled Out
- **H1: JFK ATC Sequencing Caused Missed Connection (Code ATC-14)** -> `FALSIFIED`: 14m ATC spacing alone leaves 63m layover at LHR, exceeding the 45m minimum connection time by 18 minutes. (Refuted by: `zetaris_rest.faa_metar_atc#METAR-KJFK-1019`)
- **H2: Controllable 41m Catering & Gate Staffing Hold (OPS-CAT-19)** -> `VERIFIED_ROOT_CAUSE`: Removing the 41m controllable gate hold preserves the connection; under Folkerts, final arrival delay (248m) governs payout. (Refuted by: `N/A`)

## 4. Counterfactual Flip Thresholds (What Flips This Decision?)
- **Controllable Catering Hold** (Actual: `41 min`) -> Flip at `<= 18 min`: Passenger arrives at LHR with >= 45 min MCT, catches CDG flight, and delay payout flips to $0.
- **JFK ATC Spacing Hold** (Actual: `14 min`) -> Flip at `>= 33 min (alone breaking 45m MCT)`: ATC becomes independent sufficient cause of missed connection ($650 cash -> $0).
- **Rebooked Paris Arrival Delay** (Actual: `248 min`) -> Flip at `180 to 239 min (-9 min faster)`: Article 7(2) 50% reduction applies, cutting cash compensation from $650 to $325.

## 6. Meterless Nightshift & NVIDIA Nemotron Model Receipts
| Step | Agent | Lane | Model Handled By | Latency |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Intake & Statutory Scope Agent | Lane 1 (Fast Worker) | `nvidia/nemotron-3.5-lightning-30b-a3b` | 225.0 ms |
| 2 | Telemetry Forensics Agent (Round 1 SQL) | Lane 1 (Fast Worker) | `nvidia/nemotron-3.5-lightning-30b-a3b` | 223.0 ms |
| 3 | Devil's Advocate Airline Counsel Critic | Lane 2 (Deep Worker) | `nvidia/nemotron-3.5-super-vl-120b-a12b` | 445.0 ms |
| 4 | Telemetry Forensics Agent (Round 2 Tail & Crew SQL) | Lane 1 (Fast Worker) | `nvidia/nemotron-3.5-lightning-30b-a3b` | 229.0 ms |
| 5 | Counterfactual & Threshold Boundary Engine | Lane 2 (Deep Worker) | `nvidia/nemotron-3.5-super-vl-120b-a12b` | 444.0 ms |
| 6 | Explainable Legal Brief & Claim Packet Agent | Lane 2 (Deep Worker) | `nvidia/nemotron-3.5-super-vl-120b-a12b` | 434.0 ms |

## 7. Ready-to-Send Passenger Notice
```text
DEMAND FOR EU261/UK261 COMPENSATION ($715.00) - CLAIM CLM-9088 / FLIGHT BA-112 (JFK->LHR->CDG)
1. METAR-KJFK-1019 shows JFK ATC spacing accounted for only 14 minutes, leaving 63m of a 77m connection (above 45m MCT).
2. Operational log OPS-CAT-19 confirms 41m controllable catering and boarding delay caused the 9-minute connection miss.
3. Under EU261 Art. 7 & Folkerts (C-11/11) for 248m final arrival delay at CDG, remit $650 (€600) + $65 Art. 9 meals = $715.00.
```
