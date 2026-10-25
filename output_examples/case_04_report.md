# SurgeWhy Explainable Adjudication Report: CASE-04 (LH-455)

- **Claim ID:** `CLM-9132` | **Route:** `FRA -> SFO` | **Carrier:** Lufthansa
- **Airline Initial Decision:** `CLAIM DENIED ($0 PAYOUT): Departure delayed by Frankfurt Airport mandatory de-icing queue, and aircraft touched down less than 3 hours late (Code WX-DEICE).`
- **SurgeWhy Verdict:** **PAUSED AT 62% CONFIDENCE: 1 DOCUMENT NEEDED TO UNLOCK $325**
- **Calibrated Confidence:** `62%` | **Abstention Gate:** `True`

## 1. Plain-English Why
SurgeWhy proved 108 minutes of your delay was a controllable emergency-light bus repair (MNT-4482), defeating Lufthansa's de-icing excuse! However, SurgeWhy refuses to guess on your payout yet: under EU law (Germanwings v. Henning), the 180-minute cliff for €300 ($325) is measured at the exact minute the cabin door opens. Because wheel-stop was +177m ($0) and jetbridge dock was +184m ($325) - a 7-minute sensor gap right across the 180m line - one timestamped arrival screenshot flips this claim to a 96%-confident $325 win.

## 2. Cited Causal Proof Chain
- **1. Airline Claim:** Denied citing Frankfurt de-icing queue & touchdown <180m (Code WX-DEICE) (`[zetaris_ops.flight_disruptions#CLM-9132]`)
- **2. De-Icing Excuse Defeated:** Tail D-ABYA had 108m controllable cabin light bus repair before 76m de-icing queue (`[zetaris_maint.aircraft_crew_logs#MNT-4482]`)
- **3. Legal Cliff Identified:** Henning (C-452/13) measures 180m cliff at cabin door open, NOT touchdown/wheel-stop (`[zetaris_policy.passenger_rights_rules#EU261-HENNING-DOOR]`)
- **4. Calibrated Abstention Gate:** 184m +/-7m spans [177m ($0) .. 184m ($325)] -> Confidence 62% < 75% gate -> Request 1 proof (`[zetaris_ops.flight_disruptions#CLM-9132]`)

## 3. Hypotheses Tested & Ruled Out
- **H1: De-Icing Queue Solely Caused Delay (Code WX-DEICE)** -> `FALSIFIED`: 108m of the delay was a controllable MEL-33-12 emergency-lighting bus reboot at the gate. (Refuted by: `zetaris_maint.aircraft_crew_logs#MNT-4482`)
- **H2: Cabin Door Opened >= 180 Minutes After Scheduled Arrival** -> `AMBIGUOUS_BOUNDARY`: ACARS wheel-stop (+177m) vs jetbridge sensor (+184m) leaves a 7-minute uncertainty window across the 180m cliff. (Refuted by: `zetaris_ops.flight_disruptions#CLM-9132`)

## 4. Counterfactual Flip Thresholds (What Flips This Decision?)
- **Verified Cabin Door-Open Timestamp** (Actual: `177m to 184m (+/-7m uncertainty)`) -> Flip at `Confirmed >= 180 min (uncertainty = 0)`: Confidence jumps from 62% to 96% and verdict flips from ABSTAIN to OVERTURNED ($325 / €300 payout).
- **Verified Cabin Door-Open Timestamp** (Actual: `177m to 184m (+/-7m uncertainty)`) -> Flip at `Confirmed <= 179 min`: Falls 1 minute short of EU261 3-hour threshold; statutory payout locks at $0.

## 5. Missing Evidence Request (Human Verification Gate)
> Upload 1 timestamped proof of SFO cabin door-open time (e.g., phone photo EXIF in jetbridge, cellular 'Welcome to USA' SMS, or flight-attendant log) resolving the 7-minute gap between wheel-stop (+177m) and jetbridge dock (+184m).

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
EVIDENCE HOLD - CLAIM CLM-9132 / FLIGHT LH-455 (FRA->SFO)
Status: PAUSED AT 62% CONFIDENCE (Calibrated Abstention Gate Active).
Causal Liability Proven: Log MNT-4482 confirms 108m controllable MEL-33-12 repair.
Action Required From Passenger: Provide 1 timestamped record proving cabin door opened >=180m past scheduled arrival to unlock $325 (€300) demand.
```
