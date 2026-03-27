# Compositing Patterns

These are the code patterns for layering animated overlays on top of the original video. These patterns were refined through real production use and solve specific problems (symlink issues, video positioning).

## Table of Contents

1. [FinalComposition.tsx](#finalcompositiontsx) — The core compositing wrapper
2. [transcript.ts](#transcriptts) — Segment format for scene timing
3. [theme.ts](#themets) — Shared constants
4. [Root.tsx](#roottsx) — Composition registration with all 6 entries
5. [MainVideo pattern](#mainvideo-pattern) — TransitionSeries wrapper for each version

---

## FinalComposition.tsx

This component composites two layers into a 1080x1920 frame:
1. The raw video (shifted down so the speaker's head appears below the overlay)
2. The animated overlay (1080x1080, positioned at the top)

The `VIDEO_OFFSET_Y` value must be calculated per-video based on where the speaker's head is. See the main SKILL.md for how to determine this.

```tsx
import React from "react";
import { OffthreadVideo, staticFile } from "remotion";

// Hair top in original video: ~y=420 out of 1920
// We want hair top at y=1080 (bottom of overlay area)
// So video offset = 1080 - 420 = 660
const VIDEO_OFFSET_Y = 660;

interface FinalCompositionProps {
  OverlayComponent: React.FC;
}

export const FinalComposition: React.FC<FinalCompositionProps> = ({
  OverlayComponent,
}) => {
  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        position: "relative",
        overflow: "hidden",
        backgroundColor: "#000000",
      }}
    >
      {/* Raw video — shifted down so hair top aligns with y=1080 */}
      <div
        style={{
          position: "absolute",
          top: VIDEO_OFFSET_Y,
          left: 0,
          width: 1080,
          height: 1920,
        }}
      >
        <OffthreadVideo
          src={staticFile("raw.MOV")}
          style={{ width: 1080, height: 1920 }}
        />
      </div>

      {/* Overlay — top 1080x1080 */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: 1080,
          height: 1080,
        }}
      >
        <OverlayComponent />
      </div>
    </div>
  );
};
```

### Key decisions in this pattern

- **`OffthreadVideo`** instead of `<Video>`: OffthreadVideo renders video frames in a separate thread, which is important for render performance. It avoids the main thread blocking on video decode.
- **`staticFile("raw.MOV")`**: Remotion serves files from `public/` via `staticFile()`. The file must be physically present (not a symlink) because the webpack bundler copies files to a temp directory.
- **`overflow: "hidden"`**: The video is 1920px tall but shifted down by VIDEO_OFFSET_Y, so the bottom portion extends beyond the frame. Hidden overflow clips it cleanly.
- **`backgroundColor: "#000000"`**: Black fill for any gaps (though with correct offset calculation there shouldn't be visible gaps).

---

## transcript.ts

Timestamped segments from whisper output, used for timing overlay scenes to match the speaker's words.

```typescript
export const TRANSCRIPT_SEGMENTS = [
  { start: 0.0, end: 1.6, text: "If you're not using slash commands" },
  { start: 1.6, end: 3.1, text: "in Claude Code, you're still a rookie." },
  { start: 3.1, end: 5.2, text: "Here are 3 you should start with." },
  { start: 5.2, end: 6.4, text: "First, clear." },
  { start: 6.4, end: 8.2, text: "It clears the entire conversation history" },
  { start: 8.2, end: 10.2, text: "giving you a clean context window." },
  // ... continue for all segments
];
```

---

## theme.ts

Centralizes the design system and timing constants. The timing values must be calculated based on the specific video's transcript.

```typescript
import { loadFont } from "@remotion/google-fonts/Inter";
import { loadFont as loadHeading } from "@remotion/google-fonts/DMSans";
import { Easing } from "remotion";

const { fontFamily: interFamily } = loadFont("normal", {
  weights: ["400", "500", "600", "700"],
  subsets: ["latin"],
});

const { fontFamily: dmSansFamily } = loadHeading("normal", {
  weights: ["500", "600", "700"],
  subsets: ["latin"],
});

export const FONT = interFamily;          // Body — labels, data, credentials
export const FONT_HEADING = dmSansFamily; // Headings — key metrics, titles

export const COLORS = {
  heroDark: "#1A1A2E",       // Deep charcoal-navy — hero sections
  lightBg: "#FAFAFA",        // Clean off-white — content sections
  cardBg: "#FFFFFF",         // Pure white — cards
  textOnDark: "#FFFFFF",     // Text on dark backgrounds
  textOnLight: "#1A1A1A",    // Text on light backgrounds
  textMuted: "#6B7280",      // Secondary text
  textMeta: "#9CA3AF",       // Labels, credentials
  accentBlue: "#3B82F6",     // Primary accent — highlights, underlines
  accentTeal: "#14B8A6",     // Secondary accent — success, positive data
  border: "#E5E7EB",         // Dividers, card borders
};

// Easing curves — NO spring() or bounce
export const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const EASE_IN_OUT = Easing.bezier(0.4, 0, 0.2, 1);

// Shared timing constants
export const FPS = 30;
export const TRANSITION = 10; // frames of overlap between scenes

// Calculate these based on the video:
// TOTAL_FRAMES = videoDurationSeconds * FPS
// SCENE_DURATIONS = calculated from transcript breakpoints using TransitionSeries math
// Target ~2s per scene (60 frames at 30fps) for fast, engaging pacing
export const TOTAL_FRAMES = 810; // example: 27s * 30fps
export const SCENE_DURATIONS = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 70]; // example: ~14 scenes for 27s video
```

### TransitionSeries timing math

Given desired scene start times (in frames) from the transcript:
```
d1 = startTime[scene2] + T
d2 = startTime[scene3] - startTime[scene2] + T
d3 = startTime[scene4] - startTime[scene3] + T
...
dN = totalFrames - startTime[sceneN]
```

Where `T` is the TRANSITION duration (10 frames). Verify: `sum(durations) - (numScenes - 1) * T = TOTAL_FRAMES`.

---

## Root.tsx

Registers all 6 compositions — 3 overlay-only previews (1080x1080) and 3 final composited renders (1080x1920).

```tsx
import React from "react";
import { Composition } from "remotion";
import { MainVideoV1 } from "./v1/MainVideoV1";
import { MainVideoV2 } from "./v2/MainVideoV2";
import { MainVideoV3 } from "./v3/MainVideoV3";
import { FinalComposition } from "./FinalComposition";
import { TOTAL_FRAMES, FPS } from "./theme";

const FinalV1: React.FC = () => (
  <FinalComposition OverlayComponent={MainVideoV1} />
);
const FinalV2: React.FC = () => (
  <FinalComposition OverlayComponent={MainVideoV2} />
);
const FinalV3: React.FC = () => (
  <FinalComposition OverlayComponent={MainVideoV3} />
);

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Overlay-only previews (1080x1080) */}
      <Composition
        id="V1"
        component={MainVideoV1}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={1080}
        height={1080}
      />
      <Composition
        id="V2"
        component={MainVideoV2}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={1080}
        height={1080}
      />
      <Composition
        id="V3"
        component={MainVideoV3}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={1080}
        height={1080}
      />

      {/* Final renders (1080x1920 TikTok vertical) */}
      <Composition
        id="FinalV1"
        component={FinalV1}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
      />
      <Composition
        id="FinalV2"
        component={FinalV2}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
      />
      <Composition
        id="FinalV3"
        component={FinalV3}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
      />
    </>
  );
};
```

---

## MainVideo pattern

Each version's MainVideo wraps its scenes in a TransitionSeries with fade transitions. This pattern is the same across all 3 versions — only the imported scene components differ.

```tsx
import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { TRANSITION, SCENE_DURATIONS } from "../theme";
import { HookScene } from "./scenes/HookScene";
import { ClearScene } from "./scenes/ClearScene";
import { CompactScene } from "./scenes/CompactScene";
import { SimplifyScene } from "./scenes/SimplifyScene";
import { CTAScene } from "./scenes/CTAScene";

const scenes = [
  { Component: HookScene, duration: SCENE_DURATIONS[0] },
  { Component: ClearScene, duration: SCENE_DURATIONS[1] },
  { Component: CompactScene, duration: SCENE_DURATIONS[2] },
  { Component: SimplifyScene, duration: SCENE_DURATIONS[3] },
  { Component: CTAScene, duration: SCENE_DURATIONS[4] },
];

export const MainVideoV1: React.FC = () => {
  return (
    <TransitionSeries>
      {scenes.map((scene, i) => {
        const { Component } = scene;
        return (
          <React.Fragment key={i}>
            <TransitionSeries.Sequence durationInFrames={scene.duration}>
              <Component />
            </TransitionSeries.Sequence>
            {i < scenes.length - 1 && (
              <TransitionSeries.Transition
                presentation={fade()}
                timing={linearTiming({ durationInFrames: TRANSITION })}
              />
            )}
          </React.Fragment>
        );
      })}
    </TransitionSeries>
  );
};
```

The scene names here are just examples — name scenes based on what they represent in the transcript content.
