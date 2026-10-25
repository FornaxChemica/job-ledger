import React from "react";
import { C, fonts } from "../styles/tokens";
import { LedgerLabel } from "./Cards";
import { Icon } from "./Icons";
import { profile as p } from "../data/sampleProfile";
export const ApplicationDashboard = () => (
  <div
    style={{
      background: C.ivory,
      padding: 48,
      borderRadius: 30,
      borderTop: `9px solid ${C.forest}`,
      boxShadow: "0 30px 80px #17352620",
      fontFamily: fonts.document,
      color: C.charcoal,
    }}
  >
    <LedgerLabel />
    <div
      style={{
        fontFamily: fonts.editorial,
        fontSize: 67,
        lineHeight: 1.1,
        marginTop: 16,
      }}
    >
      Your applications.
    </div>
    <div style={{ fontSize: 29, color: C.muted, marginTop: 13 }}>
      One clear place to pick up.
    </div>
    <div style={{ marginTop: 42 }}>
      {["Ready to review", "Needs your action"].map((label) => (
        <div
          key={label}
          style={{
            borderTop: `1px solid ${C.line}`,
            padding: "24px 0",
            display: "flex",
            justifyContent: "space-between",
            fontSize: 34,
            color: C.muted,
          }}
        >
          <span>{label}</span>
          <span style={{ fontSize: 28 }}>Nothing waiting</span>
        </div>
      ))}
    </div>
    <div
      style={{
        borderTop: `1px solid ${C.line}`,
        paddingTop: 28,
        fontSize: 34,
        color: C.forest,
        display: "flex",
        alignItems: "center",
        gap: 13,
      }}
    >
      <Icon name="check" size={30} />
      Applied
    </div>
    <div
      style={{
        background: C.paper,
        border: `1px solid ${C.line}`,
        borderRadius: 18,
        padding: 29,
        marginTop: 18,
      }}
    >
      <div style={{ fontSize: 44, fontFamily: fonts.editorial }}>
        {p.employer}
      </div>
      <div style={{ fontSize: 32, marginTop: 9 }}>{p.role}</div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 28,
          color: C.forest,
          marginTop: 24,
        }}
      >
        <span>Confirmation recorded</span>
        <span>{p.reference}</span>
      </div>
    </div>
    <div style={{ fontSize: 27, color: C.muted, marginTop: 31 }}>
      Illustrative snapshot · sample data
    </div>
  </div>
);
