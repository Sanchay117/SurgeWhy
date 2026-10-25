import React from "react";
import { Img, staticFile, useCurrentFrame } from "remotion";
import { C, FONT } from "../theme";

interface GlassBrowser3DProps {
  screenFile: string;
  urlText?: string;
  rotateYDeg?: number;
  rotateXDeg?: number;
  scale?: number;
  width?: number;
  height?: number;
  accentColor?: string;
  statusPill?: string;
}

export const GlassBrowser3D: React.FC<GlassBrowser3DProps> = ({
  screenFile,
  urlText = "http://127.0.0.1:8060 // surgewhy-explainability-studio",
  rotateYDeg = -11,
  rotateXDeg = 3,
  scale = 1,
  width = 1080,
  height = 675,
  accentColor = C.sky,
  statusPill = "TRACK 2 // EXPLAIN WHY",
}) => {
  const frame = useCurrentFrame();
  const sheenPos = ((frame * 1.3) % 240) - 60;

  return (
    <div
      style={{
        width,
        height,
        transform: `perspective(1550px) rotateY(${rotateYDeg}deg) rotateX(${rotateXDeg}deg) scale(${scale})`,
        transformStyle: "preserve-3d",
        borderRadius: 20,
        background: "rgba(8, 13, 25, 0.94)",
        border: "1px solid rgba(56, 189, 248, 0.26)",
        boxShadow: `0 44px 105px rgba(0, 0, 0, 0.82), 0 0 60px ${accentColor}26`,
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        position: "relative",
      }}
    >
      <div
        style={{
          height: 42,
          padding: "0 18px",
          background: "linear-gradient(180deg, #13203B 0%, #0B1325 100%)",
          borderBottom: "1px solid rgba(56, 189, 248, 0.16)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ width: 11, height: 11, borderRadius: "50%", background: "#F43F5E" }} />
          <span style={{ width: 11, height: 11, borderRadius: "50%", background: "#F59E0B" }} />
          <span style={{ width: 11, height: 11, borderRadius: "50%", background: "#10B981" }} />
        </div>
        <div
          style={{
            padding: "4px 16px",
            borderRadius: 7,
            background: "rgba(5, 9, 20, 0.72)",
            border: "1px solid rgba(255,255,255,0.09)",
            fontFamily: FONT.mono,
            fontSize: 11.5,
            color: C.inkDim,
          }}
        >
          {urlText}
        </div>
        <div
          style={{
            padding: "4px 10px",
            borderRadius: 6,
            background: "rgba(16, 185, 129, 0.16)",
            border: "1px solid rgba(16, 185, 129, 0.4)",
            fontFamily: FONT.mono,
            fontSize: 10.5,
            fontWeight: 700,
            color: "#6EE7B7",
          }}
        >
          {statusPill}
        </div>
      </div>

      <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>
        <Img
          src={staticFile(screenFile)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "top center",
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(115deg, transparent ${sheenPos - 18}%, rgba(255,255,255,0.05) ${sheenPos}%, transparent ${sheenPos + 18}%)`,
            pointerEvents: "none",
          }}
        />
      </div>
    </div>
  );
};
