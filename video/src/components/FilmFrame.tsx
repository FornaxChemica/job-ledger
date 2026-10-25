import React from "react";
import { AbsoluteFill } from "remotion";
import { C } from "../styles/tokens";
import { smooth, useSeconds } from "./Motion";
export const FilmBackground: React.FC<{ warm?: boolean }> = ({
  warm = false,
}) => (
  <AbsoluteFill
    style={{
      background: warm
        ? C.ivory
        : "linear-gradient(155deg,#f8fbff 0%,#edf4ff 48%,#d9e9fb 100%)",
    }}
  >
    <div
      style={{
        position: "absolute",
        width: 1400,
        height: 1400,
        left: 240,
        top: 740,
        border: "1px solid #8faed328",
        borderRadius: "50%",
      }}
    />
    <div
      style={{
        position: "absolute",
        width: 1650,
        height: 1650,
        left: 115,
        top: 615,
        border: "1px solid #8faed318",
        borderRadius: "50%",
      }}
    />
  </AbsoluteFill>
);
export const Headline: React.FC<{
  lines: string[];
  at?: number;
  size?: number;
  accent?: boolean;
  style?: React.CSSProperties;
}> = ({ lines, at = 0, size = 83, accent = true, style }) => {
  const t = useSeconds();
  const p = smooth(t, at, at + 0.38);
  return (
    <div
      style={{
        position: "absolute",
        left: 86,
        right: 86,
        top: 185,
        color: C.ink,
        fontFamily: "Inter",
        fontWeight: 600,
        fontSize: size,
        lineHeight: 1.08,
        letterSpacing: -4.1,
        opacity: p,
        transform: `translateY(${(1 - p) * 24}px)`,
        ...style,
      }}
    >
      {lines.map((line, i) => (
        <div
          key={line}
          style={{
            color: accent && i === lines.length - 1 ? C.blueInk : undefined,
          }}
        >
          {line}
        </div>
      ))}
    </div>
  );
};
export const FilmChrome: React.FC<{ phase?: string; safe?: boolean }> = ({
  phase,
  safe,
}) => (
  <>
    <div
      style={{
        position: "absolute",
        top: 91,
        left: 86,
        right: 86,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        fontFamily: "Inter",
        fontSize: 25,
        letterSpacing: 2,
        color: "#516578",
      }}
    >
      <span style={{ fontWeight: 600 }}>
        CUBBIE{" "}
        <span style={{ fontWeight: 400, color: "#8a9aa9", margin: "0 12px" }}>
          /
        </span>{" "}
        JOB LEDGER
      </span>
      <span style={{ fontSize: 20, letterSpacing: 1.2 }}>{phase}</span>
    </div>
    <div
      style={{
        position: "absolute",
        left: 86,
        bottom: 118,
        display: "flex",
        gap: 12,
        alignItems: "center",
        fontFamily: "Inter",
        fontSize: 27,
        color: "#4b6175",
      }}
    >
      <span
        style={{
          width: 7,
          height: 7,
          borderRadius: "50%",
          background: "#6b8093",
        }}
      />
      Illustrative demo
    </div>
    {safe && (
      <div
        style={{
          position: "absolute",
          inset: "120px 96px 230px 80px",
          border: "3px dashed #e44570",
          pointerEvents: "none",
        }}
      >
        <span style={{ fontSize: 26, color: "#e44570", background: "white" }}>
          Social-safe guides · preview only
        </span>
      </div>
    )}
  </>
);
