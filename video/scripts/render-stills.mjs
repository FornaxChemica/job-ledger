import { bundle } from "@remotion/bundler";
import {
  selectComposition,
  renderStill,
  openBrowser,
} from "@remotion/renderer";
import fs from "node:fs/promises";
import path from "node:path";
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const browser = await openBrowser("chrome", {
  browserExecutable: "/usr/bin/chromium",
  chromiumOptions: { gl: "angle" },
});
try {
  const composition = await selectComposition({
    serveUrl,
    id: "JobLedgerLaunch",
    puppeteerInstance: browser,
  });
  await fs.mkdir("output/stills", { recursive: true });
  for (const [name, second] of [
    ["hook", 2],
    ["background", 6.6],
    ["opportunity", 10.8],
    ["tailoring", 19.4],
    ["review", 25.9],
    ["approval", 33],
    ["dashboard", 37],
    ["end", 41],
  ]) {
    await renderStill({
      serveUrl,
      composition,
      puppeteerInstance: browser,
      frame: Math.round(second * 60),
      output: `output/stills/${name}.png`,
      imageFormat: "png",
      chromiumOptions: { gl: "angle" },
    });
    console.log(name, second);
  }
} finally {
  await browser.close({ silent: true });
}
