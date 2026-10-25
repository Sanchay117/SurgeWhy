# SurgeWhy Explainable Adjudication Report: CASE-05 (AA-204)

- **Claim ID:** `CLM-9175` | **Route:** `DFW -> ORD` | **Carrier:** American Airlines
- **Airline Initial Decision:** `CLAIM DENIED ($0 PAYOUT): Aircraft equipment swap required by regional airspace congestion; passenger transported to destination in Economy (Code ATC-SWAP).`
- **SurgeWhy Verdict:** **OVERTURNED: PAY $1,140 ($960 Cabin Downgrade + $180 Bag Fee)**
- **Calibrated Confidence:** `98%` | **Abstention Gate:** `False`

## 1. Plain-English Why
American Airlines claimed 'regional airspace congestion' (Code ATC-SWAP) forced an aircraft change, but FAA telemetry shows clear skies and zero flow restrictions between Dallas and Chicago. Operational log OPS-SWAP-77 proves airline revenue management pulled your healthy Boeing 787 (tail N814AA) to fly a high-margin sports charter (AA-9940) and substituted a smaller plane with 12 fewer Business seats, entitling you to a 75% Business fare refund ($960) plus 100% refund of the $180 bag fee ($1,140 total).

## 2. Cited Causal Proof Chain
- **1. Airline Claim:** Denied citing ATC-SWAP airspace congestion equipment change ($0 paid) (`[zetaris_ops.flight_disruptions#CLM-9175]`)
- **2. Airspace Clear:** KDFW & KORD had 10.0 SM visibility, 0 ground stops, 19/20 peer departures on time (`[zetaris_rest.faa_metar_atc#METAR-KDFW-1022]`)
- **3. Commercial Charter Swap:** Healthy B787 tail N814AA reassigned to charter AA-9940; narrowbody sub cut 12 Business seats (`[zetaris_maint.aircraft_crew_logs#OPS-SWAP-77]`)
- **4. Downgrade & Fee Rule:** 75% of $1,280 Business fare ($960) + $180 included Business bag fee = $1,140 (`[zetaris_policy.passenger_rights_rules#DOT-DOWNGRADE-75]`)

## 3. Hypotheses Tested & Ruled Out
- **H1: Regional Airspace Congestion Forced Equipment Swap (ATC-SWAP)** -> `FALSIFIED`: Zero FAA congestion advisories existed, and tail N814AA had zero mechanical defects. (Refuted by: `zetaris_rest.faa_metar_atc#METAR-KDFW-1022, zetaris_maint.aircraft_crew_logs#OPS-SWAP-77`)
- **H2: Commercial Charter Reassignment + Involuntary Cabin Downgrade** -> `VERIFIED_ROOT_CAUSE`: Commercial fleet reassignment triggers mandatory involuntary downgrade refund (75% segment fare) and ancillary fee reversal. (Refuted by: `N/A`)

## 4. Counterfactual Flip Thresholds (What Flips This Decision?)
- **Substituted Cabin Seat** (Actual: `Downgraded Business -> Economy`) -> Flip at `Accommodated in Business Class on next flight`: $960 downgrade refund and $180 bag fee flip to $0.
- **Swap Reason (OPS-SWAP-77)** (Actual: `Commercial reassignment to charter AA-9940`) -> Flip at `Safety-driven swap (even if weather/ATC)`: IMPORTANT: Even in safety swaps, involuntary cabin downgrade STILL requires refunding fare difference + $180 Business bag allowance!

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
DEMAND FOR INVOLUNTARY DOWNGRADE & FEE REFUND ($1,140.00) - CLAIM CLM-9175 / FLIGHT AA-204 (DFW->ORD)
1. METAR-KDFW-1022 and log OPS-SWAP-77 confirm healthy B787 tail N814AA was commercially reassigned to charter AA-9940.
2. Passenger paid $1,280 Business Class fare (which includes checked baggage) and was involuntarily seated in Economy.
3. Under US DOT Refund Rule & tariff downgrade rules, remit $960.00 (75% downgrade refund) + $180.00 bag fee = $1,140.00.
```
