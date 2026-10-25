# SurgeWhy Explainable Adjudication Report: CASE-03 (DL-809)

- **Claim ID:** `CLM-9104` | **Route:** `ATL -> MIA` | **Carrier:** Delta Air Lines
- **Airline Initial Decision:** `CLAIM DENIED ($0 PAYOUT): Flight DL-809 canceled due to severe thunderstorm microburst and FAA Ground Stop (Code WX-99); $310 rebooking fare difference non-refundable.`
- **SurgeWhy Verdict:** **SPLIT VERDICT: WEATHER UPHELD ($0 DELAY CASH) -> REFUND $310 UNLAWFUL FARE SURGE**
- **Calibrated Confidence:** `96%` | **Abstention Gate:** `False`

## 1. Plain-English Why
Honest split verdict: Delta was telling the truth about the storm - NOAA METAR and FAA Ground Stop GS-ATL-09 confirm a severe 54-knot microburst grounded 30 of 32 flights in Atlanta, so $0 cash delay compensation is owed. HOWEVER, charging you a $310 surge fare difference to rebook into the same Economy cabin after a flight cancellation violates Contract of Carriage Rule 24 and DOT rebooking protections, so Delta owes an immediate $310 refund.

## 2. Cited Causal Proof Chain
- **1. Airline Claim:** Canceled under WX-99 severe storm; refused refund of $310 rebooking fare surge (`[zetaris_ops.flight_disruptions#CLM-9104]`)
- **2. Storm Verified True:** KATL hit by 54kt microburst, 0.5 SM visibility, 142m FAA Ground Stop GS-ATL-09 (30/32 grounded) (`[zetaris_rest.faa_metar_atc#METAR-KATL-1020]`)
- **3. Aircraft Confirmed Clean:** Tail N342DN had zero MEL mechanical faults and fresh crew (WX-GND-91) (`[zetaris_maint.aircraft_crew_logs#WX-GND-91]`)
- **4. Surge Fee Unlawful:** Rule 24 & 14 CFR Part 260 prohibit same-cabin fare-difference charges on canceled flights -> Refund $310 (`[zetaris_policy.passenger_rights_rules#DOT-2024-REBOOK]`)

## 3. Hypotheses Tested & Ruled Out
- **H1: Extraordinary Microburst & FAA Ground Stop (Delay Cash Defense)** -> `UPHELD_AIRLINE`: 54kt microburst and mandatory FAA Ground Stop GS-ATL-09 legally excuse delay compensation ($0 cash). (Refuted by: `N/A`)
- **H2: Unlawful $310 Dynamic Fare-Surge on Involuntary Same-Cabin Rebooking** -> `VERIFIED_ROOT_CAUSE`: Even in extraordinary weather, involuntary same-cabin rebooking onto next available carrier flight must be $0 fare difference. (Refuted by: `N/A`)

## 4. Counterfactual Flip Thresholds (What Flips This Decision?)
- **Cabin Selected on Rebooking** (Actual: `Same Cabin (Economy -> Economy)`) -> Flip at `Voluntary Passenger Upgrade to First Class`: If passenger voluntarily selected First Class when Economy seats were open, the $310 fare difference becomes valid ($310 -> $0).
- **Root Cancellation Cause** (Actual: `FAA Ground Stop GS-ATL-09 (Weather)`) -> Flip at `Controllable Crew or Mechanical Cancellation`: Unlocks additional DOT controllable hotel/meal/ground-transport reimbursement on top of the $310 surge refund.

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
NOTICE OF UNLAWFUL IROPS FARE-DIFFERENCE CHARGE ($310.00) - CLAIM CLM-9104 / FLIGHT DL-809 (ATL->MIA)
1. We confirm METAR-KATL-1020 & GS-ATL-09 substantiate extraordinary weather; $0 delay compensation is claimed.
2. However, billing $310.00 fare difference for involuntary same-cabin Economy rebooking after carrier cancellation violates Rule 24.
3. Refund $310.00 to original payment method within 7 business days per 14 CFR Part 260.
```
