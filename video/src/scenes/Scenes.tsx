import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ChromeFrame } from "../components/ChromeFrame";
import { GlassBrowser3D } from "../components/GlassBrowser3D";
import { C, FONT } from "../theme";

export const OpenScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 18, stiffness: 90 } });
  const rotY = interpolate(frame, [0, 360], [-14, -5], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 20% 20%, #0E2346 0%, #050914 65%)" }}>
      <ChromeFrame
        chapterNum="01"
        chapterTitle="WHEN THE AIRLINE BOT SAYS DENIED ($0)"
        activeLayerBadge="TRACK 2 // EXPLAIN WHY"
      />
      <div
        style={{
          position: "absolute",
          top: 138,
          left: 56,
          right: 56,
          bottom: 92,
          display: "grid",
          gridTemplateColumns: "0.84fr 1.16fr",
          gap: 34,
          alignItems: "center",
        }}
      >
        <div style={{ opacity: enter, transform: `translateY(${(1 - enter) * 28}px)` }}>
          <div
            style={{
              display: "inline-block",
              padding: "6px 12px",
              borderRadius: 8,
              background: "rgba(244, 63, 94, 0.14)",
              border: "1px solid rgba(244, 63, 94, 0.42)",
              fontFamily: FONT.mono,
              fontSize: 12,
              fontWeight: 700,
              color: "#FDA4AF",
              marginBottom: 18,
            }}
          >
            FLIGHT UA-418 · SFO -&gt; LHR · DELAYED 4H 25M
          </div>
          <h1
            style={{
              fontFamily: FONT.display,
              fontSize: 52,
              fontWeight: 900,
              lineHeight: 1.07,
              letterSpacing: "-0.03em",
              color: C.ink,
              marginBottom: 18,
            }}
          >
            The bot blamed <span style={{ color: C.rose }}>weather</span>.{" "}
            <span style={{ color: C.sky }}>SurgeWhy</span> proves what really happened.
          </h1>
          <p style={{ fontSize: 19, lineHeight: 1.52, color: C.inkDim, marginBottom: 24 }}>
            Auditable causal chains, ruled-out airline defenses, live counterfactual flip sliders, and calibrated uncertainty gates.
          </p>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            <div style={{ padding: 16, borderRadius: 14, background: "rgba(244,63,94,0.09)", border: "1px solid rgba(244,63,94,0.35)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11, color: "#FDA4AF" }}>AIRLINE AUTO-DENIAL</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: C.rose, marginTop: 4 }}>$0 Paid</div>
              <div style={{ fontSize: 12.5, color: C.inkDim, marginTop: 2 }}>Code WX-88: Hub Weather</div>
            </div>
            <div style={{ padding: 16, borderRadius: 14, background: "rgba(16,185,129,0.11)", border: "1px solid rgba(16,185,129,0.4)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11, color: "#6EE7B7" }}>SURGEWHY PROOF</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: C.emerald, marginTop: 4 }}>$890 Owed</div>
              <div style={{ fontSize: 12.5, color: C.inkDim, marginTop: 2 }}>MEL-32-41 + Crew Timeout</div>
            </div>
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "center" }}>
          <GlassBrowser3D
            screenFile="screens/causal-proof-studio.png"
            rotateYDeg={rotY}
            scale={0.96}
            accentColor={C.sky}
            statusPill="CAUSAL PROOF // CLM-9041"
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const ZetarisGraphScene: React.FC = () => {
  const frame = useCurrentFrame();
  const rotY = interpolate(frame, [0, 360], [11, 4], { extrapolateRight: "clamp" });

  const sources = [
    { code: "zetaris_ops", title: "Airline Gate & Excuse Log", val: "UA-418: Claimed WX-88 ($0)", col: C.rose },
    { code: "zetaris_rest", title: "Live NOAA METAR & ATC REST", val: "10.0 SM Clear · 14/14 Peers On Time", col: C.sky },
    { code: "zetaris_maint", title: "Tail N784UA MEL & Crew Log", val: "148m Brake Sensor + 117m Crew Timeout", col: C.emerald },
    { code: "zetaris_policy", title: "Statutory Passenger Rights", val: "UK261 Art. 7 + Art. 9 = $890", col: C.violet },
  ];

  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 80% 25%, #0D2744 0%, #050914 68%)" }}>
      <ChromeFrame
        chapterNum="02"
        chapterTitle="LAYER 01 (DATA): ZETARIS FEDERATED AVIATION SQL"
        activeLayerBadge="01 DATA // ZETARIS REST SQL"
      />
      <div
        style={{
          position: "absolute",
          top: 138,
          left: 56,
          right: 56,
          bottom: 92,
          display: "grid",
          gridTemplateColumns: "1.14fr 0.86fr",
          gap: 32,
          alignItems: "center",
        }}
      >
        <div style={{ display: "flex", justifyContent: "center" }}>
          <GlassBrowser3D
            screenFile="screens/zetaris-sql-workbench.png"
            urlText="POST http://localhost:8888/api/v1.0/sql-editor/sqls/run"
            rotateYDeg={rotY}
            scale={0.95}
            accentColor={C.emerald}
            statusPill="SINGLE-STATEMENT SQL"
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <div style={{ fontFamily: FONT.mono, fontSize: 12, color: C.sky, letterSpacing: "0.08em" }}>
            4 FEDERATED SOURCES QUERIED VIA ZETARIS
          </div>
          <h2 style={{ fontFamily: FONT.display, fontSize: 38, fontWeight: 800, color: C.ink, lineHeight: 1.12 }}>
            Cross-examining the gate excuse with real telemetry.
          </h2>
          {sources.map((s, idx) => {
            const op = interpolate(frame, [idx * 14, idx * 14 + 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            return (
              <div
                key={s.code}
                style={{
                  opacity: op,
                  padding: "13px 16px",
                  borderRadius: 13,
                  background: "rgba(12, 21, 40, 0.9)",
                  borderLeft: `4px solid ${s.col}`,
                  borderTop: "1px solid rgba(255,255,255,0.08)",
                  borderRight: "1px solid rgba(255,255,255,0.08)",
                  borderBottom: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontWeight: 700, fontSize: 15, color: C.ink }}>{s.title}</span>
                  <span style={{ fontFamily: FONT.mono, fontSize: 11.5, color: s.col }}>{s.code}</span>
                </div>
                <div style={{ fontFamily: FONT.mono, fontSize: 13, color: C.inkDim }}>{s.val}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const CounterfactualScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const showAbstention = frame > durationInFrames * 0.54;
  const rotY = interpolate(frame, [0, durationInFrames], [-10, -3], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 25% 75%, #12283A 0%, #050914 68%)" }}>
      <ChromeFrame
        chapterNum="03"
        chapterTitle="COUNTERFACTUAL FLIP LAB & CALIBRATED ABSTENTION"
        activeLayerBadge="TRACK 2 // WHAT FLIPS THE VERDICT?"
        rightMetric={showAbstention ? "LH-455 · 62% CONFIDENCE · PAUSED FOR 1 PHOTO" : "COUNTERFACTUAL DELTA // -26 MIN FLIPS TIER"}
      />
      <div
        style={{
          position: "absolute",
          top: 138,
          left: 56,
          right: 56,
          bottom: 92,
          display: "grid",
          gridTemplateColumns: "0.84fr 1.16fr",
          gap: 32,
          alignItems: "center",
        }}
      >
        <div>
          <div style={{ fontFamily: FONT.mono, fontSize: 12, color: showAbstention ? C.amber : C.emerald, marginBottom: 10 }}>
            {showAbstention ? "CALIBRATED UNCERTAINTY GATE (< 75%)" : "INTERACTIVE COUNTERFACTUAL BOUNDARIES"}
          </div>
          <h2 style={{ fontFamily: FONT.display, fontSize: 40, fontWeight: 900, color: C.ink, lineHeight: 1.1, marginBottom: 16 }}>
            {showAbstention
              ? "Refuses to guess when 7 minutes separate $0 from $325."
              : "Every verdict shows the exact change that flips it."}
          </h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <div style={{ padding: 15, borderRadius: 13, background: "rgba(15, 25, 48, 0.88)", border: "1px solid rgba(56,189,248,0.28)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11.5, color: C.sky }}>COUNTERFACTUAL 01 · ARRIVAL CLIFF</div>
              <div style={{ fontSize: 14.5, color: C.ink, marginTop: 4 }}>
                265m -&gt; <b>&lt;= 239m (-26m faster)</b> cuts UK261 cash 50% ($650 -&gt; $325).
              </div>
            </div>
            <div style={{ padding: 15, borderRadius: 13, background: "rgba(15, 25, 48, 0.88)", border: "1px solid rgba(16,185,129,0.32)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11.5, color: C.emerald }}>COUNTERFACTUAL 02 · STORM GROUND STOP</div>
              <div style={{ fontSize: 14.5, color: C.ink, marginTop: 4 }}>
                Active FAA Ground Stop flips cash $650 -&gt; $0, while <b>$240 Art. 9 hotel care stays owed</b>.
              </div>
            </div>
            <div style={{ padding: 15, borderRadius: 13, background: "rgba(245, 158, 11, 0.12)", border: "1px solid rgba(245,158,11,0.45)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11.5, color: C.amber }}>ABSTENTION GATE · FLIGHT LH-455 (62% CONF)</div>
              <div style={{ fontSize: 14.5, color: C.ink, marginTop: 4 }}>
                Wheel-stop (+177m) vs jetbridge (+184m) spans 180m Henning door rule -&gt; asks for 1 timestamped photo.
              </div>
            </div>
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "center" }}>
          <GlassBrowser3D
            screenFile={showAbstention ? "screens/calibrated-abstention-gate.png" : "screens/counterfactual-flip-lab.png"}
            rotateYDeg={rotY}
            scale={0.96}
            accentColor={showAbstention ? C.amber : C.emerald}
            statusPill={showAbstention ? "62% CONFIDENCE // HOLD" : "WHAT-IF SIMULATOR"}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const EnginesCounselScene: React.FC = () => {
  const frame = useCurrentFrame();
  const rotY = interpolate(frame, [0, 360], [10, 3], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 75% 25%, #1C1B42 0%, #050914 68%)" }}>
      <ChromeFrame
        chapterNum="04"
        chapterTitle="LAYER 02 (BUILD): CURSOR + 4 METERLESS ENGINES + COUNSEL CRITIC"
        activeLayerBadge="02 BUILD // 4 METERLESS ENGINES"
        rightMetric="MARKOVIAN: -91.3% TOKENS · WORLD MODEL v11"
      />
      <div
        style={{
          position: "absolute",
          top: 138,
          left: 56,
          right: 56,
          bottom: 92,
          display: "grid",
          gridTemplateColumns: "1.14fr 0.86fr",
          gap: 32,
          alignItems: "center",
        }}
      >
        <div style={{ display: "flex", justifyContent: "center" }}>
          <GlassBrowser3D
            screenFile="screens/counsel-and-engines.png"
            rotateYDeg={rotY}
            scale={0.95}
            accentColor={C.violet}
            statusPill="STEP 3 CRITIC // REJECTED R1"
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 13 }}>
          <div style={{ fontFamily: FONT.mono, fontSize: 12, color: C.violet }}>
            NON-LINEAR ADVERSARIAL LOOP + ALL 4 METERLESS ENGINES
          </div>
          <h2 style={{ fontFamily: FONT.display, fontSize: 36, fontWeight: 900, color: C.ink, lineHeight: 1.12 }}>
            Built to survive the airline's defense lawyer.
          </h2>
          <div style={{ padding: 14, borderRadius: 12, background: "rgba(244,63,94,0.10)", border: "1px solid rgba(244,63,94,0.42)" }}>
            <div style={{ fontFamily: FONT.mono, fontSize: 11, color: "#FDA4AF" }}>STEP 3 · AIRLINE COUNSEL CRITIC REJECTS ROUND 1</div>
            <div style={{ fontSize: 13.5, color: C.ink, marginTop: 4 }}>
              "Clear SFO skies alone don't defeat knock-on bird strike or prior-leg ATC defenses! Query tail N784UA logs."
            </div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
            <div style={{ padding: 12, borderRadius: 11, background: "rgba(12,21,40,0.9)", border: "1px solid rgba(56,189,248,0.24)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11, color: C.sky }}>SCOUT INTENT</div>
              <div style={{ fontSize: 13, color: C.inkDim, marginTop: 3 }}>Dispute routing & boundary risk gate</div>
            </div>
            <div style={{ padding: 12, borderRadius: 11, background: "rgba(12,21,40,0.9)", border: "1px solid rgba(56,189,248,0.24)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11, color: C.sky }}>WORLD MODEL v11</div>
              <div style={{ fontSize: 13, color: C.inkDim, marginTop: 3 }}>Optimistic lock hypothesis graph</div>
            </div>
            <div style={{ padding: 12, borderRadius: 11, background: "rgba(12,21,40,0.9)", border: "1px solid rgba(16,185,129,0.3)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11, color: C.emerald }}>MARKOVIAN (-91.3%)</div>
              <div style={{ fontSize: 13, color: C.inkDim, marginTop: 3 }}>Bounded &lt;=380-tok proof capsules</div>
            </div>
            <div style={{ padding: 12, borderRadius: 11, background: "rgba(12,21,40,0.9)", border: "1px solid rgba(167,139,250,0.3)" }}>
              <div style={{ fontFamily: FONT.mono, fontSize: 11, color: C.violet }}>H-MEM 3-TIER</div>
              <div style={{ fontSize: 13, color: C.inkDim, marginTop: 3 }}>Recalls & saves carrier pretexts</div>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const NemotronOutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const rotY = interpolate(frame, [0, 360], [-10, -4], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 30% 30%, #0E2B34 0%, #050914 68%)" }}>
      <ChromeFrame
        chapterNum="05"
        chapterTitle="LAYER 03 (POWER): METERLESS NIGHTSHIFT & NVIDIA NEMOTRON"
        activeLayerBadge="03 POWER // NEMOTRON 30B + 120B"
        rightMetric="3/3 SMOKE PASS · 9/9 TESTS OK"
      />
      <div
        style={{
          position: "absolute",
          top: 138,
          left: 56,
          right: 56,
          bottom: 92,
          display: "grid",
          gridTemplateColumns: "0.85fr 1.15fr",
          gap: 32,
          alignItems: "center",
        }}
      >
        <div>
          <div style={{ fontFamily: FONT.mono, fontSize: 12, color: C.emerald, marginBottom: 10 }}>
            METERLESS NIGHTSHIFT RUNTIME · DUAL NEMOTRON LANES
          </div>
          <h2 style={{ fontFamily: FONT.display, fontSize: 40, fontWeight: 900, color: C.ink, lineHeight: 1.1, marginBottom: 16 }}>
            Verifiable model receipts on every single step.
          </h2>
          <div style={{ padding: 14, borderRadius: 12, background: "rgba(12,21,40,0.9)", border: "1px solid rgba(56,189,248,0.3)", marginBottom: 12 }}>
            <div style={{ fontFamily: FONT.mono, fontSize: 11.5, color: C.sky }}>LANE 1 · FAST WORKER (STEPS 1, 2, 4)</div>
            <div style={{ fontFamily: FONT.mono, fontSize: 13.5, color: C.ink, marginTop: 4 }}>nvidia/nemotron-3.5-lightning-30b-a3b</div>
          </div>
          <div style={{ padding: 14, borderRadius: 12, background: "rgba(12,21,40,0.9)", border: "1px solid rgba(167,139,250,0.38)", marginBottom: 14 }}>
            <div style={{ fontFamily: FONT.mono, fontSize: 11.5, color: C.violet }}>LANE 2 · DEEP CRITIC & FLIP ENGINE (STEPS 3, 5, 6)</div>
            <div style={{ fontFamily: FONT.mono, fontSize: 13.5, color: C.ink, marginTop: 4 }}>nvidia/nemotron-3.5-super-vl-120b-a12b</div>
          </div>
          <div style={{ fontFamily: FONT.mono, fontSize: 12.5, color: "#6EE7B7" }}>
            github.com/Sanchay117/surgewhy · Team Push And Pray
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "center" }}>
          <GlassBrowser3D
            screenFile="screens/nightshift-nemotron-receipts.png"
            urlText="http://127.0.0.1:8088/v1 // meterless-nightshift"
            rotateYDeg={rotY}
            scale={0.96}
            accentColor={C.emerald}
            statusPill="6/6 MODEL RECEIPTS"
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};
