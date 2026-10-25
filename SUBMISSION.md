# SurgeWhy - Ready-to-Paste HackOS Submission Form (Track 2)

## Repository Name
`surgewhy` (`git@github.com:Sanchay117/surgewhy.git`)

## Project Name
`SurgeWhy`

## Primary Track
`Track 2: The Agent That Can Explain Why`

## Short Tagline / One-Liner
When an airline bot blames "weather" to pay you $0, SurgeWhy queries aviation telemetry via Zetaris to prove why your flight was actually delayed, rules out false defenses, and shows the exact counterfactual change that flips the verdict.

## Project Description (1,540 characters - fits 150-2000 char limit)
Over $6.8B in valid airline delay, fare-surge, and involuntary downgrade compensation goes unpaid annually because automated carrier bots reject claims with opaque two-word codes like "Extraordinary Weather" ($0 payout). Passengers cannot see airport METAR weather, peer concourse departures, or aircraft maintenance and crew duty logs.

SurgeWhy is an explainable multi-agent compensation adjudicator built for Track 2 (The Agent That Can Explain Why). Instead of acting as a black box, every SurgeWhy verdict delivers four auditable pillars: (1) a primary-key causal chain ([schema.table#id]), (2) a ruled-out hypotheses ledger, (3) interactive counterfactual flip boundaries showing the minimum change in minutes or weather that flips OVERTURNED to DENIED, and (4) a calibrated 75% confidence gate that pauses and requests 1 specific passenger proof when sensor uncertainty straddles a legal threshold.

How Sponsor Tech Powers SurgeWhy:
- 01 DATA (Zetaris): Executes single-statement REST SQL (POST /api/v1.0/sql-editor/sqls/run with fresh UUID4 X-Request-ID) across Gate Logs, a live NOAA/FAA METAR REST table, Tail MEL/Crew Logs, and UK261/EU261/DOT Rules.
- 02 BUILD (Cursor & 4 Meterless Engines): Built with Cursor Agent Mode (AGENTS.md + .cursor/rules/surgewhy.mdc) and all 4 Meterless Engines: Scout Intent, versioned World Model with optimistic locking, Markovian proof capsules (-91.7% tokens), and 3-tier H-MEM, plus an adversarial Airline Counsel Critic.
- 03 POWER (Meterless Nightshift & NVIDIA Nemotron): Routes Fast SQL steps to nvidia/nemotron-3.5-lightning-30b-a3b and Deep Critic/Counterfactual steps to nvidia/nemotron-3.5-super-vl-120b-a12b via Nightshift with per-step model receipts.

## Files to Upload on HackOS
- **Cover Banner (`1280x720`):** `docs/surgewhy-banner-1280x720.png`
- **Pitch Deck PDF (Optional):** `docs/SurgeWhy_Pitch_Deck.pdf`
- **Demo Video (`1080p30`, `-16 LUFS` feminine `aura-2-thalia-en` narration):** `video/out/surgewhy-final.mp4`
