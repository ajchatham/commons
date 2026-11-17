// Gemini image renders for the Cap I-95 study. Usage: node render.mjs <name> <aspect> <size> <promptFile> [refImage]
// Reads GOOGLE_API_KEY from the environment (never printed). Writes out/<name>.jpg.
import fs from "node:fs";
const [name, aspect, size, promptFile, ref] = process.argv.slice(2);
const key = process.env.GOOGLE_API_KEY;
if (!key) { console.error("no key"); process.exit(1); }
const parts = [{ text: fs.readFileSync(promptFile, "utf8") }];
for (const r of (ref || "").split(",").filter(Boolean)) parts.push({ inlineData: { mimeType: "image/jpeg", data: fs.readFileSync(r).toString("base64") } });
const res = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent", {
  method: "POST",
  headers: { "content-type": "application/json", "x-goog-api-key": key },
  body: JSON.stringify({ contents: [{ parts }], generationConfig: { responseModalities: ["IMAGE"], imageConfig: { aspectRatio: aspect, imageSize: size } } }),
});
const j = await res.json();
if (!res.ok) { console.error(res.status, JSON.stringify(j).slice(0, 400)); process.exit(1); }
const img = j.candidates?.[0]?.content?.parts?.find((p) => p.inlineData);
if (!img) { console.error("no image", JSON.stringify(j).slice(0, 400)); process.exit(1); }
fs.mkdirSync(new URL("./out/", import.meta.url), { recursive: true });
const out = new URL(`./out/${name}.jpg`, import.meta.url);
fs.writeFileSync(out, Buffer.from(img.inlineData.data, "base64"));
console.log("wrote", out.pathname, img.inlineData.mimeType);
