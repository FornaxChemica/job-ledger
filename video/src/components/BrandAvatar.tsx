import React from "react";
import { Img, staticFile } from "remotion";
// Set to true only after placing a crop of the actual supplied logo at this path.
export const HAS_ORIGINAL_LOGO = true;
export const BrandAvatar: React.FC<{
  size?: number;
  style?: React.CSSProperties;
}> = ({ size = 84, style }) => (
  <div
    style={{
      width: size,
      height: size,
      borderRadius: "50%",
      overflow: "hidden",
      flexShrink: 0,
      background: "#fff",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      ...style,
    }}
  >
    {HAS_ORIGINAL_LOGO ? (
      <Img
        src={staticFile("brand/cubbie-avatar.png")}
        style={{ width: "100%", height: "100%", objectFit: "contain" }}
      />
    ) : (
      <div
        style={{
          width: "100%",
          height: "100%",
          background: "linear-gradient(#aeb6bf,#8c959f)",
          color: "#fff",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "Inter",
          fontSize: size * 0.44,
          fontWeight: 500,
        }}
      >
        C
      </div>
    )}
  </div>
);
