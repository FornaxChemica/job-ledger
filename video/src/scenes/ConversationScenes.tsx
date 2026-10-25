import React from "react";
import { IPhoneFrame, TypingIndicator } from "../components/IPhoneFrame";
import { MessageBubble } from "../components/MessageBubble";
import { Arrival, useSeconds, smooth } from "../components/Motion";
import {
  FileStack,
  ProfileCard,
  OpportunityCard,
  PackageCard,
  FinalReviewCard,
  ConfirmationCard,
} from "../components/Cards";
import { Headline } from "../components/FilmFrame";
import { copy } from "../data/conversation";
import { headlines } from "../data/storyboard";
import { C } from "../styles/tokens";
import { Icon } from "../components/Icons";
import { ReviewWorkspace } from "../components/ReviewWorkspace";
import { ApplicationDashboard } from "../components/ApplicationDashboard";

export const HookScene = () => {
  const t = useSeconds();
  return (
    <>
      <Headline lines={headlines.hook} at={-0.6} size={80} />
      <IPhoneFrame
        scale={smooth(t, 0, 1.6, 1.02, 1)}
        y={495}
        rotate={smooth(t, 0, 1.0, -1.1, 0)}
        date="iMessage · Today 9:41 AM"
      >
        <MessageBubble at={0.65} outgoing delivered>
          {copy.request}
        </MessageBubble>
        {t > 1.9 && <TypingIndicator at={1.9} />}
      </IPhoneFrame>
    </>
  );
};
export const BackgroundScene = () => {
  const t = useSeconds();
  return (
    <>
      <Headline lines={headlines.background} size={83} />
      <IPhoneFrame
        scale={smooth(t, 0, 0.5, 1, 0.79)}
        y={smooth(t, 0, 0.5, 495, 430)}
        date="Today 9:42 AM"
      >
        <FileStack at={0.1} />
        <MessageBubble at={1.15} small>
          {copy.background}
        </MessageBubble>
        <Arrival at={2.0}>
          <ProfileCard />
        </Arrival>
      </IPhoneFrame>
    </>
  );
};
export const OpportunityScene = () => {
  const t = useSeconds();
  return (
    <>
      <Headline lines={headlines.opportunity} size={101} />
      <IPhoneFrame scale={0.83} y={395} date="Today 9:50 AM">
        <div
          style={{
            transform: `translateY(${-smooth(t, 4.05, 4.45, 0, 80)}px)`,
          }}
        >
          <MessageBubble at={0.25} small>
            {copy.found}
          </MessageBubble>
          <Arrival at={1.0}>
            <OpportunityCard />
          </Arrival>
          <MessageBubble at={3.65} outgoing style={{ marginTop: 24 }}>
            {copy.prepare}
          </MessageBubble>
          <Arrival at={4.35}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 20,
                borderRadius: 26,
                padding: 24,
                background: C.ivory,
                border: `1px solid ${C.line}`,
                fontSize: 34,
                color: C.forest,
              }}
            >
              <Icon name="file" size={42} />
              Application review.html
            </div>
          </Arrival>
        </div>
      </IPhoneFrame>
    </>
  );
};
export const ReviewScene = () => {
  const t = useSeconds();
  const open = smooth(t, 1.45, 1.95);
  const close = smooth(t, 4.45, 4.95);
  const sheet = open * (1 - close);
  return (
    <>
      <Headline lines={headlines.review} size={80} />
      <IPhoneFrame scale={0.8} y={430} date="Today 9:56 AM">
        <MessageBubble at={0.08} small>
          {copy.packageReady}
        </MessageBubble>
        <Arrival at={0.9}>
          <PackageCard />
        </Arrival>
        <MessageBubble at={5} outgoing style={{ marginTop: 35 }}>
          {copy.packageApproval}
        </MessageBubble>
      </IPhoneFrame>
      {sheet > 0 && (
        <div
          style={{
            position: "absolute",
            left: 70,
            top: 450,
            width: 940,
            opacity: Math.min(1, sheet * 2),
            transform: `translateY(${(1 - sheet) * 290}px) scale(${0.63 + sheet * 0.37})`,
            transformOrigin: "50% 30%",
            boxShadow: "0 30px 90px #1b304734",
            borderRadius: 32,
          }}
        >
          <ReviewWorkspace time={t - 1.45} />
        </div>
      )}
    </>
  );
};
export const ApprovalScene = () => (
  <>
    <Headline lines={headlines.approval} size={97} />
    <IPhoneFrame scale={0.83} y={430} date="Today 9:58 AM">
      <MessageBubble at={0.3} small>
        {copy.finalReview}
      </MessageBubble>
      <Arrival at={1.05}>
        <FinalReviewCard />
      </Arrival>
      <MessageBubble at={3.25} outgoing delivered style={{ marginTop: 30 }}>
        {copy.submitApproval}
      </MessageBubble>
    </IPhoneFrame>
  </>
);
export const OutcomeScene = () => {
  const t = useSeconds();
  const expand = smooth(t, 1.75, 2.2);
  return (
    <>
      <Headline lines={headlines.outcome} size={80} />
      <IPhoneFrame scale={0.8} y={435} date="Today 10:02 AM">
        <Arrival at={0.35}>
          <ConfirmationCard />
        </Arrival>
        <MessageBubble at={1.2} small>
          Saved to your application list.
        </MessageBubble>
      </IPhoneFrame>
      {t > 1.75 && (
        <div
          style={{
            position: "absolute",
            left: 90,
            top: 470,
            width: 900,
            opacity: expand,
            transform: `translateY(${(1 - expand) * 250}px) scale(${0.8 + 0.2 * expand})`,
            transformOrigin: "top center",
          }}
        >
          <ApplicationDashboard />
        </div>
      )}
    </>
  );
};
