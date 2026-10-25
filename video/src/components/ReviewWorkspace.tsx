import React from "react";
import { Img, staticFile } from "remotion";
import { C, fonts } from "../styles/tokens";
import { Icon } from "./Icons";
import { MiniPage } from "./Cards";
import { smooth } from "./Motion";
export const ReviewWorkspace: React.FC<{ time: number }> = ({ time }) => (
  <div
    style={{
      height: 1160,
      background: C.ivory,
      borderRadius: 32,
      overflow: "hidden",
      border: `1px solid ${C.line}`,
      color: C.charcoal,
      fontFamily: fonts.document,
    }}
  >
    <div
      style={{
        height: 78,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 30px",
        borderBottom: `1px solid ${C.line}`,
        fontSize: 28,
        background: "#fffdf9",
      }}
    >
      <span style={{ color: C.blueInk }}>Done</span>
      <span>Application review</span>
      <Icon name="share" size={31} color={C.blueInk} />
    </div>
    <div style={{ height: 1000, overflow: "hidden", position: "relative" }}>
      <Img
        src={staticFile("documents/review-film.png")}
        style={{
          width: 940,
          position: "absolute",
          top: 0,
          left: 0,
          transform: `translateY(${-smooth(time, 0.65, 2.45, 0, 780)}px)`,
        }}
      />
    </div>
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: 90,
        background: C.forest,
        color: C.paper,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 35,
        borderRadius: "0 0 32px 32px",
      }}
    >
      Resume · Cover letter · Answers
    </div>
  </div>
);
