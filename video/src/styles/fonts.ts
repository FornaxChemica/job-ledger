import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";
for (const [weight, file] of [
  ["400", "Regular"],
  ["500", "Medium"],
  ["600", "Semibold"],
  ["700", "Bold"],
]) {
  loadFont({
    family: "Inter",
    url: staticFile(`fonts/Inter-${file}.woff2`),
    weight,
  });
}
loadFont({
  family: "Source Serif 4",
  url: staticFile("fonts/SourceSerif4-Regular.ttf"),
  weight: "400",
});
loadFont({
  family: "Source Sans 3",
  url: staticFile("fonts/SourceSans3-Regular.ttf"),
  weight: "400",
});
