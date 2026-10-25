import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import "./styles/fonts";
import { FilmBackground, FilmChrome } from "./components/FilmFrame";
import {
  HookScene,
  BackgroundScene,
  OpportunityScene,
  ReviewScene,
  ApprovalScene,
  OutcomeScene,
} from "./scenes/ConversationScenes";
import { TailoringSequence } from "./components/TailoringSequence";
import { BrandEndCard } from "./components/BrandEndCard";
import { beats } from "./data/storyboard";
export type FilmProps = { safeGuides: boolean };
export const LaunchFilm: React.FC<FilmProps> = ({ safeGuides }) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();
  const t = frame / fps;
  const phase =
    t < 3
      ? "01 / START"
      : t < 7.5
        ? "02 / BACKGROUND"
        : t < 12.5
          ? "03 / AFTER SEARCH"
          : t < 22
            ? "04 / TAILORING"
            : t < 28.5
              ? "05 / PACKAGE"
              : t < 34
                ? "06 / APPROVAL"
                : t < 38
                  ? "07 / AFTER SUBMISSION"
                  : "";
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <style>{`* {box-sizing:border-box;} body {margin:0;} ::-webkit-scrollbar {display:none;} `}</style>
      <FilmBackground warm={t >= 12.5 && t < 22} />
      <Sequence
        name="01 · One message"
        from={beats.hook.start * fps}
        durationInFrames={(beats.hook.end - beats.hook.start) * fps}
      >
        <HookScene />
      </Sequence>
      <Sequence
        name="02 · Supplied background"
        from={beats.background.start * fps}
        durationInFrames={(beats.background.end - beats.background.start) * fps}
      >
        <BackgroundScene />
      </Sequence>
      <Sequence
        name="03 · A role worth considering"
        from={beats.opportunity.start * fps}
        durationInFrames={
          (beats.opportunity.end - beats.opportunity.start) * fps
        }
      >
        <OpportunityScene />
      </Sequence>
      <Sequence
        name="04 · Requirement → evidence → resume"
        from={beats.tailoring.start * fps}
        durationInFrames={(beats.tailoring.end - beats.tailoring.start) * fps}
      >
        <TailoringSequence />
      </Sequence>
      <Sequence
        name="05 · Package approval"
        from={beats.review.start * fps}
        durationInFrames={(beats.review.end - beats.review.start) * fps}
      >
        <ReviewScene />
      </Sequence>
      <Sequence
        name="06 · Separate submission approval"
        from={beats.approval.start * fps}
        durationInFrames={(beats.approval.end - beats.approval.start) * fps}
      >
        <ApprovalScene />
      </Sequence>
      <Sequence
        name="07 · Confirmation then tracking"
        from={beats.outcome.start * fps}
        durationInFrames={(beats.outcome.end - beats.outcome.start) * fps}
      >
        <OutcomeScene />
      </Sequence>
      <Sequence
        name="08 · Job Ledger for Cubbie"
        from={beats.brand.start * fps}
        durationInFrames={(beats.brand.end - beats.brand.start) * fps}
      >
        <BrandEndCard />
      </Sequence>
      <FilmChrome phase={phase} safe={safeGuides} />
    </AbsoluteFill>
  );
};
