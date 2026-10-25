# SurgeWhy Explainable Adjudication Report: CASE-01 (UA-418)

- **Claim ID:** `CLM-9041` | **Route:** `SFO -> LHR` | **Carrier:** United Airlines
- **Airline Initial Decision:** `CLAIM DENIED ($0 PAYOUT): Flight UA-418 arrived 4h 25m late due to Extraordinary Weather Conditions at Departure Hub (Code WX-88).`
- **SurgeWhy Verdict:** **OVERTURNED: PAY $890 ($650 UK261 Statutory + $240 Care)**
- **Calibrated Confidence:** `97%` | **Abstention Gate:** `False`

## 1. Plain-English Why
United's 'Extraordinary Hub Weather' denial (Code WX-88) is disproved by three independent records: NOAA METAR shows 10-mile clear skies at SFO with 14 of 14 neighboring flights departing on time, inbound aircraft N784UA landed 3 minutes early from Denver, and maintenance log MNT-4410 proves the 265-minute delay was caused by a 148-minute brake temperature sensor replacement (MEL-32-41) that triggered a 117-minute FAA Part 117 pilot duty-limit timeout.

## 2. Cited Causal Proof Chain
- **1. Airline Claim:** Carrier denied claim citing WX-88 hub weather ($0 paid) (`[zetaris_ops.flight_disruptions#CLM-9041]`)
- **2. Weather Falsified:** KSFO had 10.0 SM clear skies, 8kt wind, 0 ground stops, 14/14 peer departures on time (`[zetaris_rest.faa_metar_atc#METAR-KSFO-1018]`)
- **3. True Root Cause:** Tail N784UA had 148m brake sensor fault (MEL-32-41) -> 117m pilot Part 117 timeout (`[zetaris_maint.aircraft_crew_logs#MNT-4410]`)
- **4. Statutory Entitlement:** 265m >= 240m long-haul threshold under UK261 Art. 7 & Art. 9 = $650 + $240 = $890 (`[zetaris_policy.passenger_rights_rules#UK261-ART7-LH]`)

## 3. Hypotheses Tested & Ruled Out
- **H1: Extraordinary Hub Weather at SFO (Code WX-88)** -> `FALSIFIED`: KSFO recorded 10.0 SM clear visibility, 8kt winds, zero FAA ground stops, and 14/14 Concourse G peer flights departed on schedule. (Refuted by: `zetaris_rest.faa_metar_atc#METAR-KSFO-1018`)
- **H2: Inbound Aircraft Weather or Bird Strike on Prior Leg** -> `FALSIFIED`: Tail N784UA landed 3 minutes early from Denver with zero weather holds or bird-strike inspections. (Refuted by: `zetaris_maint.aircraft_crew_logs#MNT-4410`)
- **H3: Routine Brake Sensor MEL-32-41 + Knock-On Crew Duty Timeout** -> `VERIFIED_ROOT_CAUSE`: 148m hydraulic sensor repair + 117m reserve pilot wait = 265m controllable carrier delay under Wallentin-Hermann. (Refuted by: `N/A`)

## 4. Counterfactual Flip Thresholds (What Flips This Decision?)
- **Final Arrival Delay** (Actual: `265 min`) -> Flip at `<= 239 min (-26 min faster)`: Payout drops from $890 to $565 ($325 50%-tier UK261 cash + $240 care); at <= 179 min cash drops to $0.
- **FAA Ground Stop / Crosswind** (Actual: `0 Ground Stops, 8 kt wind`) -> Flip at `Active FAA Ground Stop = 1 (or wind > 35 kt)`: Statutory cash flips from $650 to $0, BUT $240 Art. 9 hotel/meal duty-of-care STILL remains legally owed.
- **Defect Type on N784UA** (Actual: `MEL-32-41 routine brake sensor wear`) -> Flip at `Fleet-wide FAA Airworthiness Directive or Foreign Object Runway Debris`: Root cause reclassifies to Extraordinary Circumstance ($650 cash -> $0).

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
DEMAND FOR UK261 COMPENSATION ($890.00) - CLAIM CLM-9041 / FLIGHT UA-418 (SFO->LHR)
1. Carrier's WX-88 weather denial is contradicted by NOAA METAR-KSFO-1018 (10.0 SM visibility, 8kt wind, 14/14 peer departures on time).
2. Maintenance record MNT-4410 on tail N784UA confirms 148m MEL-32-41 brake sensor repair + 117m Part 117 crew timeout (265m controllable).
3. Under UK261 Art. 7(1)(c) (Wallentin-Hermann) and Art. 9, remit $650 (£520) statutory compensation + $240 verified care receipts = $890.00.
```
