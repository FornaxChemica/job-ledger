import { chromium } from "playwright";
import { createServer } from "node:http";
import path from "node:path";
import fs from "node:fs/promises";
const input =
  process.argv[2] ?? "/workspace/job-ledger/output/demo/06-package.html";
const output = process.argv[3] ?? "output/review-page.png";
await fs.mkdir(path.dirname(output), { recursive: true });
const html = await fs.readFile(input);
const server = createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end(html);
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  headless: true,
  args: ["--no-sandbox"],
});
try {
  const page = await browser.newPage({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
  });
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`, {
    waitUntil: "load",
  });
  await page.evaluate(() => document.fonts.ready);
  if (errors.length) throw new Error(errors.join("\n"));
  if (!(await page.locator("body").innerText()).trim())
    throw new Error("Empty review page");
  await page.screenshot({ path: output, fullPage: true });
  console.log(
    JSON.stringify({ title: await page.title(), screenshot: output, errors }),
  );
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
