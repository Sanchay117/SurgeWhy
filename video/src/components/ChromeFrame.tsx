import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, FONT } from "../theme";

interface ChromeFrameProps {
  chapterNum: string;
  chapterTitle: string;
  activeLayerBadge: string;
  rightMetric?: string;
}

export const ChromeFrame: React.FC<ChromeFrameProps> = ({
  chapterNum,
  chapterTitle,
  activeLayerBadge,
  rightMetric = "UA-418 SFO->LHR · $890 VERIFIED · 97% CONFIDENCE",
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 50 }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          zIndex: -1,
          backgroundImage: `
            linear-gradient(to right, rgba(56, 189, 248, 0.05) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(56, 189, 248, 0.05) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />

      {/* Top Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 52,
          right: 52,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              width: 38,
              height: 38,
              borderRadius: 10,
              background: "linear-gradient(135deg, #0284C7 0%, #38BDF8 55%, #10B981 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 0 24px rgba(56, 189, 248, 0.45)",
              fontFamily: FONT.mono,
              fontWeight: 900,
              fontSize: 15,
              color: "#04101E",
            }}
          >
            SW
          </div>
          <span
            style={{
              fontFamily: FONT.display,
              fontWeight: 800,
              fontSize: 23,
              color: C.ink,
              letterSpacing: "-0.03em",
            }}
          >
            Surge<span style={{ color: C.sky }}>Why</span>
          </span>
          <span
            style={{
              fontFamily: FONT.mono,
              fontSize: 11,
              fontWeight: 700,
              color: C.sky,
              padding: "4px 11px",
              borderRadius: 999,
              background: "rgba(56, 189, 248, 0.12)",
              border: "1px solid rgba(56, 189, 248, 0.35)",
              letterSpacing: "0.06em",
            }}
          >
            {activeLayerBadge}
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div
            style={{
              fontFamily: FONT.mono,
              fontSize: 11,
              color: C.inkDim,
              letterSpacing: "0.07em",
              padding: "6px 14px",
              borderRadius: 999,
              background: "rgba(12, 21, 40, 0.82)",
              border: "1px solid rgba(56, 189, 248, 0.18)",
            }}
          >
            01 ZETARIS · 02 CURSOR + METERLESS · 03 NIGHTSHIFT NEMOTRON
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              padding: "6px 13px",
              borderRadius: 999,
              background: "rgba(16, 185, 129, 0.14)",
              border: "1px solid rgba(16, 185, 129, 0.38)",
              fontFamily: FONT.mono,
              fontSize: 11,
              fontWeight: 700,
              color: "#6EE7B7",
            }}
          >
            <span
              style={{
                width: 7,
                height: 7,
                borderRadius: "50%",
                background: C.emerald,
                boxShadow: `0 0 ${8 + 4 * Math.sin(frame * 0.2)}px ${C.emerald}`,
              }}
            />
            {rightMetric}
          </div>
        </div>
      </div>

      {/* Bottom Corner Chapter Pill */}
      <div
        style={{
          position: "absolute",
          top: 86,
          left: 52,
          fontFamily: FONT.mono,
          fontSize: 11.5,
          color: C.inkDim,
          letterSpacing: "0.08em",
        }}
      >
        <span style={{ color: C.emerald, fontWeight: 800 }}>{chapterNum}</span> // {chapterTitle}
      </div>
    </AbsoluteFill>
  );
};
