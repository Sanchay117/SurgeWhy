import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import timingData from "./generated/timing.json";
import { SceneId } from "./narration";
import { C, FONT } from "./theme";
import {
  CounterfactualScene,
  EnginesCounselScene,
  NemotronOutroScene,
  OpenScene,
  ZetarisGraphScene,
} from "./scenes/Scenes";

const SCENE_COMPONENTS: Record<SceneId, React.FC> = {
  open: OpenScene,
  zetaris: ZetarisGraphScene,
  counterfactual: CounterfactualScene,
  engines: EnginesCounselScene,
  outro: NemotronOutroScene,
};

interface TimedLine {
  file: string;
  text: string;
  startSec: number;
  startFrame: number;
  seconds: number;
  frames: number;
}

const SceneCaptions: React.FC<{ lines: TimedLine[] }> = ({ lines }) => {
  const frame = useCurrentFrame();
  const active = lines.find(
    (l) => frame >= l.startFrame - 2 && frame <= l.startFrame + l.frames + 4
  );
  if (!active) return null;

  const localF = frame - active.startFrame;
  const op = interpolate(
    localF,
    [-2, 5, active.frames - 4, active.frames + 4],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        position: "absolute",
        bottom: 28,
        left: "50%",
        transform: "translateX(-50%)",
        maxWidth: 1020,
        padding: "8px 22px",
        borderRadius: 999,
        background: "rgba(5, 9, 20, 0.88)",
        border: "1px solid rgba(56, 189, 248, 0.25)",
        boxShadow: "0 12px 32px rgba(0, 0, 0, 0.68)",
        fontFamily: FONT.sans,
        fontSize: 15.5,
        fontWeight: 500,
        color: C.ink,
        textAlign: "center",
        opacity: op,
        zIndex: 60,
        pointerEvents: "none",
      }}
    >
      {active.text}
    </div>
  );
};

const SceneCrossfade: React.FC<{
  id: SceneId;
  frames: number;
  fadeFrames: number;
  isFirst: boolean;
  isLast: boolean;
}> = ({ id, frames, fadeFrames, isFirst, isLast }) => {
  const frame = useCurrentFrame();
  const s = (timingData.scenes as Record<string, any>)[id];
  const Comp = SCENE_COMPONENTS[id];

  const fadeIn = isFirst
    ? 1
    : interpolate(frame, [0, fadeFrames], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
  const fadeOut = isLast
    ? 1
    : interpolate(frame, [frames - fadeFrames, frames], [1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <AbsoluteFill style={{ opacity }}>
      <Comp />
      <SceneCaptions lines={s.lines} />
      {s.lines.map((l: TimedLine) => (
        <Sequence key={l.file} from={l.startFrame} layout="none">
          <Audio src={staticFile(l.file)} volume={1.0} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const Video: React.FC = () => {
  const T = timingData.transitionFrames;
  const FPS = timingData.fps;
  const order = timingData.order as SceneId[];

  let cursor = 0;
  const scheduled = order.map((id, idx) => {
    const dur = (timingData.scenes as Record<string, any>)[id].durationInFrames;
    const from = cursor;
    cursor += dur - T;
    return {
      id,
      from,
      dur,
      isFirst: idx === 0,
      isLast: idx === order.length - 1,
    };
  });

  const voiceIntervals = scheduled.flatMap((item) =>
    (timingData.scenes as Record<string, any>)[item.id].lines.map((l: TimedLine) => {
      const startSec = item.from / FPS + l.startSec;
      return [startSec, startSec + l.seconds] as const;
    })
  );
  const lastWordSec =
    voiceIntervals.length > 0
      ? voiceIntervals[voiceIntervals.length - 1][1]
      : timingData.totalDurationSec;

  const musicVolume = (f: number) => {
    const t = f / FPS;
    let duck = 0;
    for (const [a, b] of voiceIntervals) {
      if (t < a - 0.35 || t > b + 0.5) continue;
      duck = Math.max(
        duck,
        Math.min(1, (t - (a - 0.35)) / 0.35, (b + 0.5 - t) / 0.5)
      );
    }
    const tail = interpolate(t, [lastWordSec, lastWordSec + 1], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const fadeOut = interpolate(
      f,
      [timingData.totalDurationInFrames - 40, timingData.totalDurationInFrames],
      [1, 0],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    );
    return (0.14 - 0.085 * duck + 0.05 * tail) * fadeOut;
  };

  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <Audio src={staticFile("music/bed.wav")} volume={musicVolume} />
      {scheduled.map((s) => (
        <Sequence key={s.id} from={s.from} durationInFrames={s.dur}>
          <SceneCrossfade
            id={s.id}
            frames={s.dur}
            fadeFrames={T}
            isFirst={s.isFirst}
            isLast={s.isLast}
          />
          {!s.isFirst && <Audio src={staticFile("sfx/whoosh.wav")} volume={0.28} />}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
