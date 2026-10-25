-- ============================================================================
-- SurgeWhy - Zetaris Lightning SQL Source Onboarding Script
-- Run one statement at a time in the Zetaris SQL Editor (http://localhost:3000)
-- or via scripts/preflight.py +POST /api/v1.0/sql-editor/sqls/run.
-- Never batch semicolon-separated statements in a single REST request.
-- ============================================================================

-- 1. Create SchemaStore containers for SurgeWhy Unified Semantic Layer
CREATE SCHEMASTORE CONTAINER surgewhy;

CREATE SCHEMASTORE CONTAINER zetaris_ops;

CREATE SCHEMASTORE CONTAINER zetaris_maint;

CREATE SCHEMASTORE CONTAINER zetaris_policy;

CREATE SCHEMASTORE CONTAINER zetaris_rest;

-- 2. Register Live FAA / NOAA METAR & ATC Ground Stop REST Database
CREATE LIGHTNING DATABASE SURGEWHY_FAA_REST DESCRIBE BY "Live NOAA METAR weather and FAA ATC Ground Stop telemetry feed";

CREATE LIGHTNING REST TABLE faa_metar_atc FROM SURGEWHY_FAA_REST REQUEST (
  endpoint "http://host.docker.internal:8060/api/mock-faa-metar",
  method "get",
  response_type "json",
  http_encoding "URLENCODED"
) HEADER () BODY ();

-- 3. Register Starter PokeAPI Check (Participant Setup Guide Page 10)
CREATE LIGHTNING DATABASE POKEAPI_REST DESCRIBE BY "Starter PokeAPI verification recipe";

CREATE SCHEMASTORE CONTAINER pokeapi;

CREATE LIGHTNING REST TABLE pikachu_facts FROM POKEAPI_REST REQUEST (
  endpoint "https://pokeapi.co/api/v2/pokemon/pikachu",
  method "get",
  response_type "json",
  http_encoding "URLENCODED"
) HEADER () BODY ();

-- 4. Create Unified Semantic Layer federated audit view across all 4 aviation domains
CREATE SCHEMASTORE VIEW claim_audit_federated WITH CONTAINER surgewhy AS
SELECT
  f.claim_id,
  f.flight_number,
  f.carrier_name,
  f.route,
  f.actual_arr_delay_min,
  f.airline_claimed_code,
  w.visibility_sm,
  w.wind_speed_kt,
  w.faa_ground_stop_active,
  w.peer_concourse_departures_ontime,
  m.primary_event_code,
  m.primary_event_category,
  m.controllable_minutes,
  m.crew_timeout_minutes
FROM zetaris_ops.flight_disruptions f
JOIN zetaris_rest.faa_metar_atc w ON f.claim_id = w.claim_id
JOIN zetaris_maint.aircraft_crew_logs m ON f.claim_id = m.claim_id;
