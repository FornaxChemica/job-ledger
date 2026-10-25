import React from "react";
import { C } from "../styles/tokens";
import { Arrival } from "./Motion";
export const MessageBubble: React.FC<{
  children: React.ReactNode;
  at: number;
  outgoing?: boolean;
  small?: boolean;
  delivered?: boolean;
  style?: React.CSSProperties;
}> = ({
  children,
  at,
  outgoing = false,
  small = false,
  delivered = false,
  style,
}) => (
  <Arrival
    at={at}
    outgoing={outgoing}
    style={{
      display: "flex",
      alignItems: outgoing ? "flex-end" : "flex-start",
      flexDirection: "column",
      marginBottom: 22,
      ...style,
    }}
  >
    <div
      style={{
        position: "relative",
        maxWidth: 650,
        background: outgoing ? C.blue : C.iosGray,
        color: outgoing ? "white" : "#111",
        fontSize: small ? 40 : 46,
        lineHeight: 1.23,
        letterSpacing: -0.9,
        padding: "21px 28px",
        borderRadius: 42,
        borderBottomRightRadius: outgoing ? 13 : 42,
        borderBottomLeftRadius: outgoing ? 42 : 13,
        boxSizing: "border-box",
      }}
    >
      <svg
        width="22"
        height="30"
        viewBox="0 0 22 30"
        style={{
          position: "absolute",
          bottom: 0,
          ...(outgoing ? { right: -7 } : { left: -7, transform: "scaleX(-1)" }),
        }}
      >
        <path
          d="M0 0 C8 4 14 14 10 21 C12 26 17 28 22 29 C12 31 3 27 0 22 Z"
          fill={outgoing ? C.blue : C.iosGray}
        />
      </svg>
      <span style={{ position: "relative" }}>{children}</span>
    </div>
    {delivered && (
      <div
        style={{
          fontSize: 23,
          color: "#929299",
          marginTop: 9,
          marginRight: 9,
          fontWeight: 500,
        }}
      >
        Delivered
      </div>
    )}
  </Arrival>
);
