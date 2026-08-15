#!/usr/bin/env node

/** Render the canonical ID01, ID03, and ID14 composition recipes. */

import { createServer } from "node:http";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "@playwright/test";

const root = resolve(fileURLToPath(new URL("../../", import.meta.url)));
const output = resolve(process.argv[2] || join(root, "tmp", "style-preset-renders"));
const template = await readFile(join(root, "assets", "portfolio-template.html"), "utf8");

const presets = [
  ["workshop-orange", "WORKSHOP / PROCESS FIRST"],
  ["instrument-blue", "INSTRUMENT / TECHNICAL PROOF"],
  ["material-green", "MATERIAL / HUMAN EXPERIENCE"],
  ["gallery-red", "GALLERY / FORM & CRAFT"],
];
const layouts = ["ID01", "ID03", "ID08", "ID10", "ID13", "ID14", "ID16"];

const sharedValues = {
  "[PORTFOLIO THESIS]": "Light that adapts.",
  "[PROJECT NAME]": "Modular desk lamp",
  "[PORTFOLIO META]": "Fictional case · concept direction",
  "[EVIDENCE QUESTION]": "Three desk modes, one light.",
  "[EVIDENCE IMAGE 1]": "/showcase/modular-desk-lamp/images/generated/lamp-04-scenarios-sheet.webp",
  "[EVIDENCE IMAGE 2]": "/showcase/modular-desk-lamp/images/generated/lamp-06-concepts-sheet.webp",
  "[EVIDENCE IMAGE 3]": "/showcase/modular-desk-lamp/images/generated/lamp-08-cmf.webp",
  "[EVIDENCE DESCRIPTION 1]": "Fictional task-lighting scenario visualization",
  "[EVIDENCE DESCRIPTION 2]": "Fictional desk-lamp concept directions",
  "[EVIDENCE DESCRIPTION 3]": "Fictional desk-lamp CMF study",
  "[EVIDENCE CAPTION 1]": "E0 · scenario hypothesis · not research evidence",
  "[EVIDENCE CAPTION 2]": "E0 · concept alternatives · selection to validate",
  "[EVIDENCE CAPTION 3]": "E0 · CMF intent · not material approval",
  "[EVIDENCE TAKEAWAY]": "The case needs adaptable light placement without adding visual clutter.",
  "[FINAL VALUE PROPOSITION]": "One base. Three modes.",
  "[FINAL PRODUCT IMAGE]": "/showcase/modular-desk-lamp/images/generated/lamp-12-final-hero.webp",
  "[FINAL PRODUCT DESCRIPTION]": "Fictional modular desk lamp final concept",
  "[FINAL STATUS]": "E0 · AI-assisted concept visualization · not a physical prototype",
  "[FINAL TAKEAWAY]": "A replaceable light module keeps the desk calm while supporting different work modes.",
  "[CMF TITLE]": "Precision without visual noise.",
  "[CMF IMAGE]": "/showcase/modular-desk-lamp/images/generated/lamp-08-cmf.webp",
  "[CMF IMAGE DESCRIPTION]": "Fictional modular desk lamp CMF detail",
  "[CMF STATUS]": "E0 · AI-assisted visualization · not material approval",
  "[CMF RATIONALE]": "Deep navy carries the structure; cobalt makes the replaceable module legible.",
  "[SWATCH 1]": "#10233e",
  "[SWATCH 2]": "#1c67d2",
  "[SWATCH 3]": "#f4f0df",
  "[MATERIAL 1]": "matte aluminum",
  "[MATERIAL 2]": "replaceable sleeve",
  "[MATERIAL 3]": "warm opal diffuser",
  "[ARCHITECTURE TITLE]": "Separate what ages differently.",
  "[ARCHITECTURE IMAGE]": "/showcase/modular-desk-lamp/images/generated/lamp-09-conceptual-architecture.webp",
  "[ARCHITECTURE DESCRIPTION]": "Conceptual exploded illustration of the modular desk lamp",
  "[ARCHITECTURE STATUS]": "Conceptual architecture illustration · not engineering evidence",
  "[COMPONENT 1]": "replaceable light head",
  "[COMPONENT 2]": "two-stage arm",
  "[COMPONENT 3]": "cylindrical joints",
  "[COMPONENT 4]": "serviceable base",
  "[ARCHITECTURE TAKEAWAY]": "The concept separates light, motion, power, and service paths.",
  "[ITERATION TITLE]": "Wider base. Shorter reach.",
  "[ITERATION IMAGE 1]": "/showcase/modular-desk-lamp/images/generated/lamp-11-iteration-pair.webp",
  "[ITERATION IMAGE 2]": "/showcase/modular-desk-lamp/images/generated/lamp-11-iteration-pair.webp",
  "[ITERATION DESCRIPTION 1]": "Earlier fictional lamp concept",
  "[ITERATION DESCRIPTION 2]": "Revised fictional lamp concept",
  "[ITERATION CAPTION 1]": "Before · narrow base and long lower arm",
  "[ITERATION CAPTION 2]": "After · proposed wider base and shorter arm",
  "[ITERATION TAKEAWAY]": "The revision responds to a stability concern; physical validation is still required.",
  "[PROJECT NUMBER]": "01",
  "[PROJECT THESIS]": "One repairable platform for task light, call light, and compact storage.",
  "[PROJECT META]": "Fictional concept proposition · E0",
};

function fill(fragment, label) {
  let html = fragment.replaceAll("[SYSTEM LABEL]", label);
  for (const [placeholder, value] of Object.entries(sharedValues)) {
    html = html.replaceAll(placeholder, value);
  }
  return html;
}

async function renderDocument(preset, label) {
  const fragments = await Promise.all(
    layouts.map((layout) => readFile(join(root, "assets", "compositions", preset, `${layout}.html`), "utf8")),
  );
  return template
    .replace("[STYLE_PRESET]", preset)
    .replaceAll("[PORTFOLIO_TITLE]", "Style System Comparison")
    .replaceAll("[DESIGNER_NAME]", "Industrial Design Portfolio")
    .replaceAll("[PORTFOLIO_META]", preset)
    .replace("<!-- PORTFOLIO_SLIDES -->", fragments.map((fragment) => fill(fragment, label)).join("\n"));
}

const documents = new Map();
for (const [preset, label] of presets) {
  documents.set(`/__style-preview/${preset}.html`, await renderDocument(preset, label));
}

const mime = new Map([
  [".html", "text/html; charset=utf-8"],
  [".webp", "image/webp"],
  [".png", "image/png"],
  [".json", "application/json; charset=utf-8"],
]);

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url || "/", "http://127.0.0.1");
    if (documents.has(url.pathname)) {
      response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
      response.end(documents.get(url.pathname));
      return;
    }
    const candidate = resolve(root, `.${decodeURIComponent(url.pathname)}`);
    if (candidate !== root && !candidate.startsWith(`${root}\\`) && !candidate.startsWith(`${root}/`)) {
      response.writeHead(403).end("Forbidden");
      return;
    }
    const body = await readFile(candidate);
    response.writeHead(200, { "content-type": mime.get(extname(candidate)) || "application/octet-stream" });
    response.end(body);
  } catch {
    response.writeHead(404).end("Not found");
  }
});

await mkdir(output, { recursive: true });
await new Promise((resolveListen) => server.listen(0, "127.0.0.1", resolveListen));
const address = server.address();
const origin = `http://127.0.0.1:${address.port}`;
const browser = await chromium.launch({ headless: true });

try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  for (const [preset] of presets) {
    await page.goto(`${origin}/__style-preview/${preset}.html?render=all`, { waitUntil: "networkidle" });
    await page.waitForFunction(() => [...document.images].every((image) => (
      image.complete && image.naturalWidth > 0 && (!image.dataset.src || image.currentSrc.endsWith(".webp"))
    )));
    await page.evaluate(() => Promise.all([...document.images].map((image) => image.decode())));
    await page.addStyleTag({ content: ".chrome,.progress{display:none!important}" });
    const deckSlides = page.locator(".slide");
    for (const [index, layout] of layouts.entries()) {
      await deckSlides.nth(index).screenshot({ path: join(output, `${preset}-${layout}.png`), type: "png" });
    }
  }
  await page.setViewportSize({ width: 390, height: 844 });
  for (const [preset] of presets) {
    await page.goto(`${origin}/__style-preview/${preset}.html?render=all`, { waitUntil: "networkidle" });
    const fitsViewport = await page.evaluate(() => (
      document.documentElement.scrollWidth <= document.documentElement.clientWidth
    ));
    if (!fitsViewport) throw new Error(`${preset} composition recipes overflow the 390px viewport`);
  }
  await page.close();
} finally {
  await browser.close();
  await new Promise((resolveClose, rejectClose) => server.close((error) => (error ? rejectClose(error) : resolveClose())));
}

await writeFile(join(output, "presets.json"), `${JSON.stringify(presets.map(([id]) => id), null, 2)}\n`);
console.log(`Rendered ${presets.length} systems × ${layouts.length} composition recipes to ${output}`);
