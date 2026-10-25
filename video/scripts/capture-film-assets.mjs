import { chromium } from "playwright";
import { createServer } from "node:http";
import fs from "node:fs/promises";
const packageHtml = await fs.readFile("public/documents/package.html");
const transcript = await fs.readFile("public/documents/transcript.html");
const server = createServer((req, res) => {
  res.setHeader("Content-Type", "text/html");
  res.end(req.url === "/transcript" ? transcript : packageHtml);
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
try {
  const page = await browser.newPage({
    viewport: { width: 470, height: 1000 },
    deviceScaleFactor: 2,
  });
  await page.goto(`http://127.0.0.1:${server.address().port}/`, {
    waitUntil: "load",
  });
  await page.evaluate(() => document.fonts.ready);
  // Film-only condensation of the actual generated review HTML. The original stays untouched.
  await page.addStyleTag({
    content: `
 body.packet {font-size:17px;line-height:1.25;} body.packet .topbar{padding:16px 22px;} body.packet main{padding:18px 24px 28px;}
 body.packet .mast{margin:0 0 14px;} body.packet .mast h1{font-size:36px;line-height:1.05;margin:8px 0;}
 body.packet .role{font-size:17px;margin:7px 0;} body.packet .lede,.section-hint,.eyebrow,.next-step,.skip,.paper-contact,.paper-date {display:none;}
 body.packet .packet-nav{padding:9px 0;gap:7px 15px;margin-bottom:14px;font-size:13px;}
 body.packet section{margin:18px 0 0;padding-top:10px;} body.packet h2{font-size:22px;margin:0 0 12px;} body.packet #overview{display:none;}
 body.packet .fit-row{padding:8px 0;} body.packet .paper{padding:14px;margin:8px 0;} body.packet .doc{margin-top:15px;}
 body.packet h3{font-size:20px;margin:8px 0;} body.packet .paper-name{font-size:23px;margin:0 0 10px;}
 body.packet .sheet-section{margin-top:10px;} body.packet .sheet-section h4{font-size:11px;letter-spacing:.1em;}
 body.packet .sheet-bullets{padding-left:18px;} body.packet .sheet-bullets li{margin:4px 0;}
 body.packet #documents .doc:nth-child(2) .paper{font-size:14px;}
 body.packet .letter-head,.letter-date,.letter-close,.letter-sign{display:none;}
 body.packet .letter{font-size:15px;line-height:1.35;} body.packet .letter p{margin-bottom:8px;}
 body.packet #documents{display:grid;grid-template-columns:1fr 1fr;gap:0 12px;} body.packet #documents h2{grid-column:1 / -1;} body.packet #documents .doc{min-width:0;} body.packet #documents .paper{height:250px;overflow:hidden;font-size:13px;padding:12px;} body.packet #documents .paper-name{font-size:21px;} body.packet #documents .letter{font-size:13px;} body.packet #documents .sheet-section:nth-child(2){display:none;} body.packet #review {display:none;} body.packet .qa{padding:5px 0;} body.packet .qa .caption{display:none;}
 `,
  });
  await page.screenshot({
    path: "public/documents/review-film.png",
    fullPage: true,
  });
  console.log("Captured actual rendered review layout:", await page.title());
  await page.goto(`http://127.0.0.1:${server.address().port}/transcript`);
  await page.pdf({
    path: "public/documents/Transcript.pdf",
    format: "A4",
    printBackground: true,
  });
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
