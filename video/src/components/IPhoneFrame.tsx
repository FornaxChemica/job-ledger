import React from "react";
import { C } from "../styles/tokens";
import { BrandAvatar } from "./BrandAvatar";
import { Icon } from "./Icons";
import { useSeconds, smooth } from "./Motion";
export const PHONE = {
  width: 800,
  height: 1660,
  screenInset: 14,
  contentTop: 296,
};
export const IPhoneFrame: React.FC<{
  children: React.ReactNode;
  scale?: number;
  x?: number;
  y?: number;
  rotate?: number;
  style?: React.CSSProperties;
  date?: string;
}> = ({ children, scale = 0.8, x = 540, y = 440, rotate = 0, style, date }) => (
  <div
    style={{
      position: "absolute",
      left: x - 400,
      top: y,
      width: 800,
      height: 1660,
      transform: `scale(${scale}) rotate(${rotate}deg)`,
      transformOrigin: "top center",
      borderRadius: 112,
      background:
        "linear-gradient(105deg,#b5b9c2 0%,#40454b 3%,#24272c 40%,#777d83 82%,#c7c9cc 100%)",
      padding: 7,
      boxShadow: "0 38px 65px #20364b20,0 7px 18px #1c273d26",
      ...style,
    }}
  >
    <div
      style={{
        position: "absolute",
        left: -5,
        top: 290,
        width: 7,
        height: 65,
        borderRadius: 4,
        background: "#646b73",
      }}
    />
    <div
      style={{
        position: "absolute",
        left: -5,
        top: 395,
        width: 7,
        height: 110,
        borderRadius: 4,
        background: "#646b73",
      }}
    />
    <div
      style={{
        position: "absolute",
        right: -5,
        top: 435,
        width: 7,
        height: 150,
        borderRadius: 4,
        background: "#646b73",
      }}
    />
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        borderRadius: 106,
        background: "#08090b",
        padding: 7,
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          position: "relative",
          width: "100%",
          height: "100%",
          borderRadius: 99,
          background: "#fff",
          overflow: "hidden",
          fontFamily: "Inter",
          color: "#08090b",
        }}
      >
        <StatusBar time={date?.match(/\d{1,2}:\d{2}/)?.[0] ?? "9:41"} />
        <MessagesHeader />
        <div
          style={{
            position: "absolute",
            top: 296,
            left: 0,
            right: 0,
            bottom: 162,
            overflow: "hidden",
            padding: "0 27px",
            boxSizing: "border-box",
          }}
        >
          {date && (
            <div
              style={{
                textAlign: "center",
                fontSize: 25,
                color: "#8a8a90",
                marginBottom: 32,
                fontWeight: 500,
              }}
            >
              {date}
            </div>
          )}
          {children}
        </div>
        <Composer />
      </div>
    </div>
  </div>
);
export const StatusBar = ({ time }: { time: string }) => (
  <div
    style={{
      height: 105,
      position: "relative",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 54px",
      fontSize: 30,
      fontWeight: 600,
    }}
  >
    <span>{time}</span>
    <div
      style={{
        position: "absolute",
        top: 22,
        left: "50%",
        transform: "translateX(-50%)",
        width: 224,
        height: 61,
        borderRadius: 40,
        background: "#08090b",
      }}
    >
      <div
        style={{
          position: "absolute",
          right: 19,
          top: 22,
          width: 17,
          height: 17,
          borderRadius: "50%",
          background: "radial-gradient(circle at 40% 40%,#1e314a,#0c111b 65%)",
        }}
      />
    </div>
    <div style={{ display: "flex", gap: 13, alignItems: "center" }}>
      <div
        style={{ display: "flex", gap: 4, alignItems: "flex-end", height: 25 }}
      >
        {[10, 15, 20, 25].map((h) => (
          <div
            key={h}
            style={{
              width: 6,
              height: h,
              borderRadius: 2,
              background: "#101216",
            }}
          />
        ))}
      </div>
      <svg
        width="34"
        height="28"
        viewBox="0 0 24 20"
        fill="none"
        stroke="#101216"
        strokeWidth="3.2"
        strokeLinecap="round"
      >
        <path d="M3 5a14 14 0 0 1 18 0M6.5 10a8 8 0 0 1 11 0M10 15a3 3 0 0 1 4 0" />
      </svg>
      <div
        style={{
          width: 43,
          height: 22,
          border: "2px solid #7e7e83",
          borderRadius: 7,
          padding: 2,
          position: "relative",
        }}
      >
        <div
          style={{ background: "#101216", height: "100%", borderRadius: 3 }}
        />
        <div
          style={{
            position: "absolute",
            right: -6,
            top: 6,
            width: 3,
            height: 8,
            background: "#7e7e83",
            borderRadius: 3,
          }}
        />
      </div>
    </div>
  </div>
);
export const MessagesHeader = () => (
  <div
    style={{
      height: 174,
      position: "relative",
      borderBottom: "1px solid #ececf0",
      background: "#fafafc",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      flexDirection: "column",
      gap: 10,
    }}
  >
    <div style={{ position: "absolute", left: 25, top: 48, color: C.blue }}>
      <Icon name="chevron" size={48} stroke={2} />
    </div>
    <BrandAvatar size={83} />
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 7,
        fontSize: 31,
        fontWeight: 500,
      }}
    >
      Cubbie <Icon name="right" size={20} color="#99999f" />
    </div>
    <div style={{ position: "absolute", right: 35, top: 54, color: C.blue }}>
      <Icon name="video" size={43} />
    </div>
  </div>
);
export const Composer = () => (
  <div
    style={{
      position: "absolute",
      bottom: 0,
      left: 0,
      right: 0,
      height: 150,
      background: "#fff",
      padding: "12px 27px",
      boxSizing: "border-box",
    }}
  >
    <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
      <div
        style={{
          width: 60,
          height: 60,
          borderRadius: 40,
          background: "#ececef",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Icon name="plus" color="#77777f" size={41} />
      </div>
      <div
        style={{
          flex: 1,
          border: "2px solid #d8d8de",
          borderRadius: 43,
          height: 75,
          display: "flex",
          alignItems: "center",
          padding: "0 24px",
          justifyContent: "space-between",
          fontSize: 34,
          color: "#a2a2a8",
        }}
      >
        iMessage
        <Icon name="mic" size={34} color="#929299" />
      </div>
    </div>
    <div
      style={{
        position: "absolute",
        bottom: 14,
        width: 270,
        height: 10,
        borderRadius: 10,
        background: "#0c0c0f",
        left: "50%",
        transform: "translateX(-50%)",
      }}
    />
  </div>
);
export const TypingIndicator: React.FC<{ at: number }> = ({ at }) => {
  const t = useSeconds();
  return (
    <div
      style={{
        display: "flex",
        gap: 12,
        alignItems: "center",
        width: 130,
        height: 70,
        padding: "0 22px",
        borderRadius: 40,
        background: C.iosGray,
        opacity: smooth(t, at, at + 0.15),
      }}
    >
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            width: 16,
            height: 16,
            borderRadius: "50%",
            background: "#949498",
            opacity:
              0.45 + 0.45 * (0.5 + 0.5 * Math.sin((t - at) * 8 - i * 1.2)),
            transform: `translateY(${-3 * Math.sin((t - at) * 8 - i * 1.2)}px)`,
          }}
        />
      ))}
    </div>
  );
};
