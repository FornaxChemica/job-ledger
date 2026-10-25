export const FPS = 60;
export const DURATION = 43;
export const beats = {
  hook: { start: 0, end: 3 },
  background: { start: 3, end: 7.5 },
  opportunity: { start: 7.5, end: 12.5 },
  tailoring: { start: 12.5, end: 22 },
  review: { start: 22, end: 28.5 },
  approval: { start: 28.5, end: 34 },
  outcome: { start: 34, end: 38 },
  brand: { start: 38, end: 43 },
} as const;
export const cues = [
  { time: 0.65, kind: "send" },
  { time: 3.25, kind: "paper" },
  { time: 4.25, kind: "receive" },
  { time: 5.0, kind: "receive" },
  { time: 7.85, kind: "receive" },
  { time: 8.55, kind: "paper" },
  { time: 11.15, kind: "send" },
  { time: 12.5, kind: "expand" },
  { time: 15.0, kind: "tick" },
  { time: 17.65, kind: "paper" },
  { time: 20.0, kind: "resolve" },
  { time: 22.1, kind: "receive" },
  { time: 23.5, kind: "expand" },
  { time: 27.0, kind: "send" },
  { time: 28.8, kind: "receive" },
  { time: 31.75, kind: "send" },
  { time: 34.4, kind: "resolve" },
  { time: 36.1, kind: "paper" },
  { time: 38.8, kind: "resolve" },
] as const;
export const headlines = {
  hook: ["Your next application", "starts with a text."],
  background: ["Your background.", "Working together."],
  opportunity: ["Find the fit."],
  review: ["One package.", "Ready for your review."],
  approval: ["You stay", "in control."],
  outcome: ["Every application.", "Accounted for."],
};
