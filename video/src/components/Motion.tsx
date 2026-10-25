import React from "react";
import {
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
export const smooth = (v: number, a: number, b: number, x = 0, y = 1) =>
  interpolate(v, [a, b], [x, y], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });
export const linear = (v: number, a: number, b: number, x = 0, y = 1) =>
  interpolate(v, [a, b], [x, y], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
export const useSeconds = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return f / fps;
};
export const Arrival: React.FC<{
  at: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
  outgoing?: boolean;
}> = ({ at, children, style, outgoing = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({
    frame: frame - at * fps,
    fps,
    config: { damping: 24, stiffness: 240, mass: 0.65 },
  });
  return (
    <div
      style={{
        opacity: linear(frame / fps, at, at + 0.12),
        transform: `translateY(${(1 - p) * 24}px) scale(${0.965 + 0.035 * p})`,
        transformOrigin: outgoing ? "bottom right" : "bottom left",
        ...style,
      }}
    >
      {children}
    </div>
  );
};
export const Reveal: React.FC<{
  at: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ at, children, style }) => {
  const t = useSeconds();
  return (
    <div
      style={{
        opacity: smooth(t, at, at + 0.3),
        transform: `translateY(${smooth(t, at, at + 0.45, 28, 0)}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
