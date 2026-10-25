import React from "react";
import { Composition } from "remotion";
import { LaunchFilm } from "./LaunchFilm";
export const Root = () => (
  <>
    <Composition
      id="JobLedgerLaunch"
      component={LaunchFilm}
      width={1080}
      height={1920}
      fps={60}
      durationInFrames={2580}
      defaultProps={{ safeGuides: false }}
    />
    <Composition
      id="JobLedgerDraft"
      component={LaunchFilm}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={1290}
      defaultProps={{ safeGuides: false }}
    />
  </>
);
