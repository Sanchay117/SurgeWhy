# SurgeWhy Aviation & Passenger Rights Datasets (`data/sample/`)

All sample datasets in `data/sample/` are synthetic, privacy-safe benchmark records modeled on public aviation and statutory standards (NOAA Aviation Weather Center METAR specifications, FAA ATCSCC Ground Stop advisories, UK261 / EU Regulation 261/2004, and 14 CFR Part 260 US DOT refund rules) created specifically for the Open Agent Hackathon 2026.

## Registered Zetaris Schemas & Tables

| Zetaris Schema & Table | Backing File (`SAMPLE_MODE=true`) | Role in Explainable Adjudication |
| :--- | :--- | :--- |
| `zetaris_ops.flight_disruptions` | `flight_disruptions.csv` | Airline gate logs, arrival delay minutes, door-open sensor uncertainty, fare-surge charges, and carrier-claimed denial codes (`WX-88`, `ATC-14`, `WX-99`, `WX-DEICE`, `ATC-SWAP`). |
| `zetaris_rest.faa_metar_atc` | `faa_metar_atc.json` | Live NOAA METAR visibility/wind telemetry + FAA Ground Stop & peer concourse departure counts registered as a Zetaris `LIGHTNING REST TABLE`. |
| `zetaris_maint.aircraft_crew_logs` | `aircraft_crew_logs.csv` | Tail-number MEL maintenance faults, FAA Part 117 crew duty timeouts, catering holds, and commercial tail swaps. |
| `zetaris_policy.passenger_rights_rules` | `passenger_rights_rules.csv` | Statutory EU261, UK261, and US DOT compensation tiers, *Wallentin-Hermann* & *Henning* legal rules, duty-of-care rules, and rebooking fare caps. |
| `pokeapi.pikachu_abilities_table` | `pikachu_abilities.csv` | Official Participant Setup Guide Page 10 starter recipe compatibility check. |
