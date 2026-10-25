import React from "react";
import { C, fonts } from "../styles/tokens";
import { profile as p } from "../data/sampleProfile";
import { smooth, linear, useSeconds } from "./Motion";
import { Headline } from "./FilmFrame";
import { LedgerLabel, MiniPage, OpportunityCard } from "./Cards";
import { IPhoneFrame } from "./IPhoneFrame";
import { MessageBubble } from "./MessageBubble";
import { copy } from "../data/conversation";
import { Icon } from "./Icons";
export const TailoringSequence = () => {
  const t = useSeconds();
  const expand = smooth(t, 0, 0.7);
  const evidence = smooth(t, 2.35, 2.75);
  const tailored = smooth(t, 5.15, 5.55);
  const resolved = smooth(t, 7.35, 7.8);
  const title =
    t < 2.5
      ? ["Reads the role."]
      : t < 5.15
        ? ["Finds your evidence."]
        : t < 7.35
          ? ["Tailors the details."]
          : ["Tailored to the job.", "Grounded in you."];
  return (
    <>
      {t < 0.7 && (
        <IPhoneFrame
          scale={0.83}
          y={395}
          date="Today 9:50 AM"
          style={{ opacity: 1 - expand }}
        >
          <div style={{ transform: "translateY(-80px)" }}>
            <MessageBubble at={-1} small>
              {copy.found}
            </MessageBubble>
            <OpportunityCard />
            <MessageBubble at={-1} outgoing style={{ marginTop: 24 }}>
              {copy.prepare}
            </MessageBubble>
          </div>
        </IPhoneFrame>
      )}
      <Headline
        key={title[0]}
        lines={title}
        at={t < 2.5 ? 0 : t < 5.15 ? 2.5 : t < 7.35 ? 5.15 : 7.35}
        size={title.length > 1 ? 80 : 84}
        accent={title.length > 1}
      />
      <div
        style={{
          position: "absolute",
          left: 85,
          top: 452 + (1 - expand) * 780,
          width: 910,
          transform: `scale(${0.62 + 0.38 * expand})`,
          transformOrigin: "50% 0%",
          opacity: linear(t, 0, 0.15),
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 77,
            left: 33,
            width: 860,
            height: 1150,
            borderRadius: 17,
            background: C.paper,
            border: `1px solid ${C.line}`,
            transform: `rotate(${3.5 * resolved}deg) translate(${28 * resolved}px,${15 * resolved}px)`,
            boxShadow: "0 16px 30px #334d3215",
          }}
        />
        <div
          style={{
            position: "relative",
            background: C.paper,
            borderRadius: 23,
            padding: "34px 45px 34px 52px",
            border: `1px solid ${C.line}`,
            boxShadow: "0 28px 65px #31422d20",
            height: 1200,
            boxSizing: "border-box",
            color: C.charcoal,
            fontFamily: fonts.document,
          }}
        >
          <LedgerLabel right="Application review · Sample data" />
          <div style={{ height: 1, background: C.line, marginBottom: 32 }} />
          <div
            style={{
              position: "absolute",
              top: 137,
              left: 41,
              width: 2,
              height: 803,
              background: C.line,
            }}
          />
          <div
            style={{
              position: "absolute",
              top: 137,
              left: 41,
              width: 2,
              height: smooth(t, 2.35, 6.0, 0, 803),
              background: C.forest,
            }}
          />
          <div style={{ position: "relative", paddingLeft: 29, height: 210 }}>
            <Step n="01" active />
            <div style={{ fontSize: 25, letterSpacing: 1.8, color: C.muted }}>
              THE ROLE · NORTHWIND LABS
            </div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 26,
                marginTop: 9,
              }}
            >
              <div
                style={{
                  fontFamily: fonts.editorial,
                  fontSize: 85,
                  lineHeight: 1.1,
                  color: C.forest,
                }}
              >
                Python
              </div>
              <div
                style={{
                  borderRadius: 28,
                  padding: "8px 16px",
                  border: `1px solid ${C.sageDeep}`,
                  fontSize: 25,
                  color: C.forest,
                }}
              >
                Requirement
              </div>
            </div>
            <div style={{ fontSize: 32, marginTop: 10, color: C.muted }}>
              Coursework or personal projects welcome.
            </div>
          </div>
          <div style={{ position: "relative", paddingLeft: 29, height: 307 }}>
            <Step n="02" active={t >= 2.35} />
            <div style={{ fontSize: 25, letterSpacing: 1.8, color: C.muted }}>
              YOUR EVIDENCE · PROJECT NOTES
            </div>
            <div
              style={{
                marginTop: 19,
                fontSize: 46,
                lineHeight: 1.23,
                letterSpacing: -0.35,
                opacity: 0.14 + 0.86 * evidence,
              }}
            >
              Built a <Mark amount={smooth(t, 2.65, 3.25)}>Python tool</Mark> to
              organize campus dining data{" "}
              <Mark amount={smooth(t, 3.0, 3.6)}>for comparison.</Mark>
            </div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 9,
                marginTop: 18,
                fontSize: 27,
                color: C.forest,
                opacity: evidence,
              }}
            >
              <Icon name="check" size={24} />
              Confirmed by Maya · from project notes
            </div>
          </div>
          <div style={{ position: "relative", paddingLeft: 29 }}>
            <Step n="03" active={t >= 5.15} />
            <div style={{ fontSize: 25, letterSpacing: 1.8, color: C.muted }}>
              YOUR RESUME · TAILORED WORDING
            </div>
            <div
              style={{
                marginTop: 19,
                borderTop: `2px solid ${C.forest}`,
                paddingTop: 18,
                opacity: 0.24 + 0.76 * tailored,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  justifyContent: "space-between",
                }}
              >
                <div style={{ fontFamily: fonts.editorial, fontSize: 47 }}>
                  Maya Chen
                </div>
                <div style={{ fontSize: 25, color: C.muted }}>PROJECTS</div>
              </div>
              <div
                style={{
                  fontSize: 31,
                  color: C.forest,
                  marginTop: 18,
                  marginBottom: 15,
                }}
              >
                Campus Dining
              </div>
              <div
                style={{
                  position: "relative",
                  fontSize: 43,
                  lineHeight: 1.25,
                  letterSpacing: -0.35,
                  minHeight: 177,
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    opacity: 1 - tailored,
                    transform: `translateY(${-tailored * 13}px)`,
                  }}
                >
                  {p.originalBullet}
                </div>
                <div
                  style={{
                    opacity: tailored,
                    transform: `translateY(${(1 - tailored) * 18}px)`,
                  }}
                >
                  Built a <Mark amount={smooth(t, 5.35, 5.9)}>Python tool</Mark>{" "}
                  to organize campus dining data for comparison.
                </div>
              </div>
              <div
                style={{
                  borderTop: `1px solid ${C.line}`,
                  paddingTop: 16,
                  marginTop: 17,
                  fontSize: 28,
                  color: C.muted,
                  opacity: smooth(t, 6.0, 6.4),
                }}
              >
                Relevant coursework: Data Structures · Databases
              </div>
            </div>
          </div>
          <div
            style={{
              position: "absolute",
              bottom: 31,
              left: 81,
              right: 44,
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              fontSize: 28,
              color: C.forest,
              opacity: resolved,
            }}
          >
            <span style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <Icon name="check" size={26} />
              Resume + cover letter
            </span>
            <span
              style={{
                background: C.sage,
                padding: "9px 16px",
                borderRadius: 20,
              }}
            >
              One review package
            </span>
          </div>
        </div>
      </div>
    </>
  );
};
const Step: React.FC<{ n: string; active: boolean }> = ({ n, active }) => (
  <div
    style={{
      position: "absolute",
      left: -25,
      top: -4,
      width: 28,
      height: 28,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      borderRadius: "50%",
      background: active ? C.forest : C.ivory,
      color: active ? "white" : C.muted,
      fontSize: 17,
      border: `1px solid ${active ? C.forest : C.line}`,
    }}
  >
    {n}
  </div>
);
const Mark: React.FC<{ amount: number; children: React.ReactNode }> = ({
  amount,
  children,
}) => (
  <span
    style={{
      background: `linear-gradient(to right,${C.sageDeep} ${amount * 100}%,transparent ${amount * 100}%)`,
      borderRadius: 5,
      padding: "0 3px",
      boxDecorationBreak: "clone",
    }}
  >
    {children}
  </span>
);
