import React from "react";
import { C } from "../styles/tokens";
import { BrandAvatar, HAS_ORIGINAL_LOGO } from "./BrandAvatar";
import { smooth, useSeconds, Reveal } from "./Motion";
import { IPhoneFrame } from "./IPhoneFrame";
import { MessageBubble } from "./MessageBubble";
import { PackageCard } from "./Cards";
export const BrandEndCard = () => {
  const t = useSeconds();
  const settle = smooth(t, 0, 0.85);
  return (
    <>
      {t < 1 && (
        <IPhoneFrame
          scale={0.8 - 0.36 * settle}
          y={435 + 120 * settle}
          rotate={-3 * settle}
          style={{ opacity: 1 - settle }}
        >
          <PackageCard />
          <MessageBubble at={-1} outgoing style={{ marginTop: 30 }}>
            My next step. Sorted.
          </MessageBubble>
        </IPhoneFrame>
      )}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: smooth(t, 0.2, 0.8),
          fontFamily: "Inter",
          textAlign: "center",
          color: C.ink,
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 260,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 22,
          }}
        >
          {HAS_ORIGINAL_LOGO && (
            <BrandAvatar
              size={108}
              style={{ boxShadow: "0 14px 35px #087ff514" }}
            />
          )}
          <span
            style={{
              fontSize: 43,
              fontWeight: 600,
              letterSpacing: -1.5,
              color: C.blueInk,
            }}
          >
            Cubbie
          </span>
        </div>
        <div style={{ position: "absolute", top: 480, left: 80, right: 80 }}>
          <div
            style={{
              fontSize: 116,
              fontWeight: 600,
              letterSpacing: -7,
              lineHeight: 1.05,
            }}
          >
            Job Ledger
          </div>
          <div
            style={{
              fontSize: 42,
              color: "#52677c",
              marginTop: 27,
              letterSpacing: -1,
            }}
          >
            A skill for Cubbie
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            top: 840,
            left: 80,
            right: 80,
            fontSize: 85,
            lineHeight: 1.09,
            fontWeight: 500,
            letterSpacing: -4.5,
          }}
        >
          Your job search.
          <br />
          <span style={{ color: C.blueInk }}>In one conversation.</span>
        </div>
        <div
          style={{
            position: "absolute",
            top: 1220,
            left: 105,
            right: 105,
            height: 118,
            borderRadius: 60,
            background: C.blue,
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 40,
            fontWeight: 600,
            letterSpacing: -1,
            boxShadow: "0 17px 34px #087ff522",
          }}
        >
          Add Job Ledger to Cubbie.
        </div>
        <div
          style={{
            position: "absolute",
            top: 1403,
            left: 80,
            right: 80,
            fontSize: 29,
            color: "#6b7b8c",
          }}
        >
          github.com/
          <div
            style={{
              fontSize: 39,
              color: C.ink,
              marginTop: 7,
              letterSpacing: -1,
            }}
          >
            FornaxChemica/job-ledger
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            top: 1570,
            left: 80,
            right: 80,
            fontSize: 34,
            color: "#52677c",
            letterSpacing: -0.6,
          }}
        >
          Text the skill link to Cubbie.
        </div>
      </div>
    </>
  );
};
