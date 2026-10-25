import React from "react";
import { C, fonts } from "../styles/tokens";
import { Icon } from "./Icons";
import { profile as p } from "../data/sampleProfile";
import { Arrival } from "./Motion";
export const LedgerLabel: React.FC<{ right?: string }> = ({
  right = "Sample data",
}) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      fontSize: 25,
      letterSpacing: 1.8,
      color: C.forest,
      marginBottom: 22,
    }}
  >
    <span>JOB LEDGER</span>
    <span style={{ fontSize: 22, letterSpacing: 0, color: C.muted }}>
      {right}
    </span>
  </div>
);
export const Surface: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ children, style }) => (
  <div
    style={{
      background: C.ivory,
      color: C.charcoal,
      borderRadius: 28,
      border: `1px solid ${C.line}`,
      borderTop: `8px solid ${C.forest}`,
      padding: 30,
      boxSizing: "border-box",
      fontFamily: fonts.document,
      ...style,
    }}
  >
    {children}
  </div>
);
export const ProfileCard = () => (
  <Surface>
    <LedgerLabel />
    <div
      style={{
        fontFamily: fonts.editorial,
        fontSize: 55,
        lineHeight: 1.1,
        marginBottom: 22,
      }}
    >
      {p.name}
    </div>
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "24px 20px",
      }}
    >
      {[
        ["EDUCATION", "Computer Science"],
        ["CONFIRMED SKILLS", "Python"],
        ["COURSEWORK", "Data Structures"],
        ["PROJECT EVIDENCE", "Campus Dining"],
      ].map(([label, value]) => (
        <div
          key={label}
          style={{ borderTop: `1px solid ${C.line}`, paddingTop: 14 }}
        >
          <div
            style={{
              fontSize: 22,
              letterSpacing: 1.4,
              color: C.muted,
              marginBottom: 9,
            }}
          >
            {label}
          </div>
          <div style={{ fontSize: 36, lineHeight: 1.15 }}>{value}</div>
        </div>
      ))}
    </div>
    <div
      style={{
        marginTop: 23,
        fontSize: 26,
        color: C.forest,
        background: C.sage,
        borderRadius: 12,
        padding: "12px 16px",
      }}
    >
      From your supplied materials
    </div>
  </Surface>
);
export const OpportunityCard = () => (
  <Surface>
    <LedgerLabel />
    <div style={{ fontFamily: fonts.editorial, fontSize: 56, lineHeight: 1.1 }}>
      {p.employer}
    </div>
    <div style={{ fontSize: 39, lineHeight: 1.15, marginTop: 10 }}>
      {p.role}
    </div>
    <div style={{ fontSize: 28, color: C.muted, marginTop: 11 }}>
      {p.location}
    </div>
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 9,
        background: C.sage,
        color: C.forest,
        borderRadius: 28,
        padding: "10px 18px",
        fontSize: 30,
        marginTop: 23,
      }}
    >
      <Icon name="check" size={25} />
      Worth considering
    </div>
    <div
      style={{
        borderTop: `1px solid ${C.line}`,
        marginTop: 25,
        paddingTop: 20,
        fontSize: 36,
        lineHeight: 1.3,
      }}
    >
      <div style={{ marginBottom: 15 }}>Python project matches the role.</div>
      <div>Coursework is welcome.</div>
    </div>
  </Surface>
);
export const FileStack: React.FC<{ at: number }> = ({ at }) => (
  <Arrival
    at={at}
    outgoing
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "flex-end",
      marginBottom: 24,
    }}
  >
    <div
      style={{
        background: "#eef4fc",
        border: "1px solid #dbe4f1",
        borderRadius: 30,
        width: 595,
        padding: "15px 23px",
      }}
    >
      {["Resume.pdf", "Transcript.pdf", "Project notes"].map((name, i) => (
        <div
          key={name}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
            padding: "12px 0",
            borderBottom: i === 2 ? "none" : "1px solid #dce5f1",
          }}
        >
          <div
            style={{
              width: 48,
              height: 57,
              borderRadius: 7,
              background: "#fff",
              color: C.blue,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Icon name="file" size={33} />
          </div>
          <div style={{ fontSize: 34, fontWeight: 500 }}>{name}</div>
          <div style={{ marginLeft: "auto", color: "#8090a2", fontSize: 21 }}>
            {i === 2 ? "TXT" : "PDF"}
          </div>
        </div>
      ))}
    </div>
  </Arrival>
);
export const MiniPage: React.FC<{
  letter?: boolean;
  style?: React.CSSProperties;
}> = ({ letter = false, style }) => (
  <div
    style={{
      width: 176,
      height: 222,
      background: C.paper,
      border: `1px solid ${C.line}`,
      boxShadow: "0 5px 15px #2837290d",
      padding: 19,
      boxSizing: "border-box",
      ...style,
    }}
  >
    <div
      style={{
        fontFamily: fonts.editorial,
        fontSize: 16,
        textAlign: "center",
        marginBottom: 14,
      }}
    >
      Maya Chen
    </div>
    <div style={{ height: 2, background: C.forest, marginBottom: 17 }} />
    {[95, 100, 85, 100, 72, 92].map((w, i) => (
      <div
        key={i}
        style={{
          height: letter ? 4 : 5,
          width: `${w}%`,
          marginBottom: letter ? 11 : 13,
          background: i === 3 ? C.sageDeep : "#d6d1c7",
        }}
      />
    ))}
    <div style={{ fontSize: 11, color: C.forest, marginTop: 14 }}>
      {letter ? "COVER LETTER" : "RESUME"}
    </div>
  </div>
);
export const PackageCard: React.FC<{ compact?: boolean }> = ({
  compact = false,
}) => (
  <Surface style={{ padding: 26 }}>
    <LedgerLabel />
    <div style={{ display: "flex", gap: 22, alignItems: "center" }}>
      <div
        style={{ position: "relative", width: 235, height: 235, flexShrink: 0 }}
      >
        <MiniPage
          letter
          style={{
            position: "absolute",
            left: 58,
            top: 4,
            transform: "rotate(6deg)",
          }}
        />
        <MiniPage
          style={{
            position: "absolute",
            left: 0,
            top: 12,
            transform: "rotate(-4deg)",
          }}
        />
      </div>
      <div>
        <div
          style={{
            fontFamily: fonts.editorial,
            fontSize: 45,
            lineHeight: 1.08,
          }}
        >
          Your review
          <br />
          package.
        </div>
        <div style={{ fontSize: 29, color: C.muted, marginTop: 15 }}>
          {p.employer}
        </div>
      </div>
    </div>
    {!compact && (
      <div
        style={{
          borderTop: `1px solid ${C.line}`,
          marginTop: 18,
          paddingTop: 18,
          fontSize: 30,
          lineHeight: 1.45,
          color: C.forest,
        }}
      >
        Resume · Cover letter · Answers
      </div>
    )}
    <div
      style={{
        marginTop: 13,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        fontSize: 25,
        color: C.muted,
      }}
    >
      <span>Application review.html</span>
      <Icon name="expand" size={26} />
    </div>
  </Surface>
);
export const FinalReviewCard = () => (
  <Surface>
    <LedgerLabel right="Final review" />
    <div style={{ fontFamily: fonts.editorial, fontSize: 51, lineHeight: 1.1 }}>
      Ready for your yes.
    </div>
    <div
      style={{
        display: "inline-block",
        background: "#ede8dd",
        padding: "10px 14px",
        borderRadius: 12,
        fontSize: 27,
        color: C.muted,
        marginTop: 19,
      }}
    >
      Filled, not submitted
    </div>
    <div style={{ marginTop: 26 }}>
      {[
        ["Earliest start", p.start],
        ["Work arrangement", "Remote, US"],
        ["Attachments", "Resume + cover letter"],
      ].map(([a, b]) => (
        <div
          key={a}
          style={{
            borderTop: `1px solid ${C.line}`,
            padding: "17px 0",
            display: "flex",
            justifyContent: "space-between",
            gap: 15,
            fontSize: 30,
          }}
        >
          <span style={{ color: C.muted }}>{a}</span>
          <span>{b}</span>
        </div>
      ))}
    </div>
    <div style={{ fontSize: 27, color: C.forest, marginTop: 10 }}>
      Review, then reply in the conversation.
    </div>
  </Surface>
);
export const ConfirmationCard = () => (
  <Surface>
    <LedgerLabel right="Sample confirmation" />
    <div
      style={{
        display: "flex",
        gap: 19,
        alignItems: "center",
        fontFamily: fonts.editorial,
        fontSize: 48,
      }}
    >
      <div
        style={{
          background: C.sage,
          borderRadius: "50%",
          width: 65,
          height: 65,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Icon name="check" size={34} color={C.forest} />
      </div>
      Application received.
    </div>
    <div style={{ fontSize: 37, marginTop: 22 }}>{p.employer}</div>
    <div style={{ fontSize: 31, color: C.muted, marginTop: 10 }}>
      Reference {p.reference}
    </div>
    <div
      style={{
        fontSize: 25,
        color: C.muted,
        borderTop: `1px solid ${C.line}`,
        marginTop: 25,
        paddingTop: 17,
      }}
    >
      Illustrative receipt · sample data
    </div>
  </Surface>
);
