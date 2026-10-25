import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SR = 48000;

function writeWav(file: string, left: Float32Array, right?: Float32Array) {
  const r = right ?? left;
  const n = left.length;
  const dataSize = n * 4;
  const buf = Buffer.alloc(44 + dataSize);
  buf.write("RIFF", 0);
  buf.writeUInt32LE(36 + dataSize, 4);
  buf.write("WAVE", 8);
  buf.write("fmt ", 12);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(2, 22);
  buf.writeUInt32LE(SR, 24);
  buf.writeUInt32LE(SR * 4, 28);
  buf.writeUInt16LE(4, 32);
  buf.writeUInt16LE(16, 34);
  buf.write("data", 36);
  buf.writeUInt32LE(dataSize, 40);
  for (let i = 0; i < n; i++) {
    const l = Math.max(-1, Math.min(1, left[i]));
    const rr = Math.max(-1, Math.min(1, r[i]));
    buf.writeInt16LE(Math.round(l * 32767), 44 + i * 4);
    buf.writeInt16LE(Math.round(rr * 32767), 44 + i * 4 + 2);
  }
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, buf);
}

let seed = 0x71b39e45;
function rand() {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return seed / 0xffffffff - 0.5;
}

function genWhoosh(): [Float32Array, Float32Array] {
  const dur = 0.48;
  const n = Math.floor(SR * dur);
  const L = new Float32Array(n);
  const R = new Float32Array(n);
  let lpL = 0,
    lpR = 0,
    phase = 0;
  for (let i = 0; i < n; i++) {
    const t = i / n;
    const env = Math.sin(Math.PI * Math.pow(t, 0.8));
    const cutoff = 0.015 + 0.14 * Math.sin(Math.PI * t);
    lpL += cutoff * (rand() * 2 - lpL);
    lpR += cutoff * (rand() * 2 - lpR);
    phase += (2 * Math.PI * (155 * Math.pow(0.45, t))) / SR;
    const sub = Math.sin(phase) * 0.22 * env;
    L[i] = (lpL * 0.36 + sub) * env * 0.52;
    R[i] = (lpR * 0.36 + sub) * env * 0.52;
  }
  return [L, R];
}

function genChime(): [Float32Array, Float32Array] {
  const dur = 0.22;
  const n = Math.floor(SR * dur);
  const L = new Float32Array(n);
  const R = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    const s =
      (Math.sin(2 * Math.PI * 659.25 * t) * 0.6 +
        Math.sin(2 * Math.PI * 987.77 * t) * 0.4) *
      Math.exp(-t * 22) *
      0.26;
    L[i] = s * 0.95;
    R[i] = s * 1.05;
  }
  return [L, R];
}

function genBed(seconds = 190): [Float32Array, Float32Array] {
  const n = SR * seconds;
  const L = new Float32Array(n);
  const R = new Float32Array(n);
  // Warm atmospheric Cmaj9 / Am11 aviation synth pad (soft, clean under speech)
  const chords = [
    [130.81, 196.0, 246.94, 293.66],
    [110.0, 164.81, 220.0, 261.63],
    [146.83, 220.0, 261.63, 329.63],
    [98.0, 146.83, 196.0, 246.94],
  ];
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    const idx = Math.floor(t / 8) % chords.length;
    const chord = chords[idx];
    const localT = (t % 8) / 8;
    const swell = 0.72 + 0.28 * Math.sin(Math.PI * localT);
    let sigL = 0;
    let sigR = 0;
    for (let k = 0; k < chord.length; k++) {
      const f = chord[k];
      sigL += Math.sin(2 * Math.PI * f * t + k * 0.4) * (0.25 / chord.length);
      sigR += Math.sin(2 * Math.PI * (f * 1.0015) * t + k * 0.9) * (0.25 / chord.length);
    }
    const pulse = 0.85 + 0.15 * Math.sin(2 * Math.PI * 2.0 * t);
    L[i] = sigL * swell * pulse * 0.45;
    R[i] = sigR * swell * pulse * 0.45;
  }
  return [L, R];
}

const sfxDir = path.resolve(__dirname, "../public/sfx");
const musicDir = path.resolve(__dirname, "../public/music");

const [wL, wR] = genWhoosh();
writeWav(path.join(sfxDir, "whoosh.wav"), wL, wR);

const [cL, cR] = genChime();
writeWav(path.join(sfxDir, "chime.wav"), cL, cR);

const [bL, bR] = genBed(190);
writeWav(path.join(musicDir, "bed.wav"), bL, bR);

console.log("Generated stereo 48kHz SFX and ambient aviation synth bed.");
