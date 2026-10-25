import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "../..");
const DOCS_DIR = path.join(ROOT, "docs");
const SCREENS_DIR = path.join(ROOT, "video/public/screens");

async function main() {
  fs.mkdirSync(DOCS_DIR, { recursive: true });
  fs.mkdirSync(SCREENS_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1600, height: 1000 },
    deviceScaleFactor: 2,
  });

  const page = await context.newPage();
  const webUrl = `file://${path.join(ROOT, "web/index.html")}`;
  await page.goto(webUrl, { waitUntil: "networkidle" });
  await page.waitForTimeout(350);

  // 1. Causal Proof & Why (CASE-01 UA-418 $890 Overturn)
  const p1 = path.join(DOCS_DIR, "causal-proof-studio.png");
  await page.screenshot({ path: p1, fullPage: false });
  fs.copyFileSync(p1, path.join(SCREENS_DIR, "causal-proof-studio.png"));
  console.log("Captured causal-proof-studio.png");

  // 2. Counterfactual Flip Lab (Tab 2)
  await page.click('[data-tab="counterfactual"]');
  await page.waitForTimeout(250);
  const p2 = path.join(DOCS_DIR, "counterfactual-flip-lab.png");
  await page.screenshot({ path: p2, fullPage: false });
  fs.copyFileSync(p2, path.join(SCREENS_DIR, "counterfactual-flip-lab.png"));
  console.log("Captured counterfactual-flip-lab.png");

  // 3. Counsel Critic & All 4 Meterless Engines (Tab 3)
  await page.click('[data-tab="engines"]');
  await page.waitForTimeout(250);
  const p3 = path.join(DOCS_DIR, "counsel-and-engines.png");
  await page.screenshot({ path: p3, fullPage: false });
  fs.copyFileSync(p3, path.join(SCREENS_DIR, "counsel-and-engines.png"));
  console.log("Captured counsel-and-engines.png");

  // 4. Nightshift & NVIDIA Nemotron Receipts (Tab 4)
  await page.click('[data-tab="power"]');
  await page.waitForTimeout(250);
  const p4 = path.join(DOCS_DIR, "nightshift-nemotron-receipts.png");
  await page.screenshot({ path: p4, fullPage: false });
  fs.copyFileSync(p4, path.join(SCREENS_DIR, "nightshift-nemotron-receipts.png"));
  console.log("Captured nightshift-nemotron-receipts.png");

  // 5. Zetaris Live SQL Workbench (Tab 5)
  await page.click('[data-tab="sql"]');
  await page.waitForTimeout(250);
  const p5 = path.join(DOCS_DIR, "zetaris-sql-workbench.png");
  await page.screenshot({ path: p5, fullPage: false });
  fs.copyFileSync(p5, path.join(SCREENS_DIR, "zetaris-sql-workbench.png"));
  console.log("Captured zetaris-sql-workbench.png");

  // 6. Calibrated 62% Abstention Gate on CASE-04 (LH-455 FRA->SFO)
  await page.click('[data-tab="why"]');
  await page.evaluate(() => {
    // @ts-ignore
    selectCase(3);
  });
  await page.waitForTimeout(250);
  const p6 = path.join(DOCS_DIR, "calibrated-abstention-gate.png");
  await page.screenshot({ path: p6, fullPage: false });
  fs.copyFileSync(p6, path.join(SCREENS_DIR, "calibrated-abstention-gate.png"));
  console.log("Captured calibrated-abstention-gate.png");

  // 7. Export 8-Slide 16:9 Pitch Deck PDF + 1280x720 Cover Banner
  const deckPage = await context.newPage();
  await deckPage.setViewportSize({ width: 1280, height: 720 });
  await deckPage.goto(`file://${path.join(ROOT, "docs/deck.html")}`, {
    waitUntil: "networkidle",
  });
  await deckPage.waitForTimeout(300);

  const bannerPath = path.join(DOCS_DIR, "surgewhy-banner-1280x720.png");
  await deckPage.screenshot({
    path: bannerPath,
    clip: { x: 0, y: 0, width: 1280, height: 720 },
  });
  console.log("Captured surgewhy-banner-1280x720.png");

  const pdfPath = path.join(DOCS_DIR, "SurgeWhy_Pitch_Deck.pdf");
  await deckPage.pdf({
    path: pdfPath,
    width: "1280px",
    height: "720px",
    printBackground: true,
    margin: { top: "0px", right: "0px", bottom: "0px", left: "0px" },
  });
  console.log("Exported SurgeWhy_Pitch_Deck.pdf");

  await browser.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
