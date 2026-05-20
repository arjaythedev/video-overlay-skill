---
name: video-overlay
description: >
  Create 3 versions of a vertical video with animated overlay graphics, ready for
  TikTok/Instagram Reels/YouTube Shorts. Use this skill whenever the user has a talking-head
  video and wants animated overlays composited on top, or wants to create multiple visual
  variations of the same video. Trigger when the user mentions "overlay on my video", "add
  graphics to my video", "TikTok video with animations", "create reels with overlays",
  "composite overlays on my talking head", or wants to produce polished vertical videos with
  animated content above the speaker. Even if the user just says "make 3 versions
  of this video with different overlays" or "add visuals on top of my video", use this skill.
  Always use the remotion-video-creator and remotion-best-practices skills alongside this one.
---

# Overlay Video Pipeline

Takes a vertical (9:16) talking-head video, creates 3 different animated overlay variations synced to the transcript, composites each overlay on top of the original video, and renders 3 final TikTok-ready MP4s. No captions are added.

The output is 3 complete 1080x1920 videos where:
- **Top half** (1080x1080): Animated overlay graphics following the brand style guide
- **Bottom half**: The speaker's head/shoulders from the original video, shifted so head sits just below the overlay

## Core Directives (Non-Negotiable)

These three rules override any conflicting guidance elsewhere in this skill, in `remotion-video-creator`, or in the brand style guide. Apply them to every scene of every version.

### 1. Open with a Hero Diagram — Never a Title Card

The first scene MUST be an animated diagram that visually previews the overarching idea of the entire video. It quickly animates in (under ~1 second to first meaningful shape, fully built by ~2 seconds) and gives the viewer the mental model the rest of the video will fill in.

The hero diagram must be *content-specific* to the video's topic. Examples:
- Video about **RAG** → animate the full RAG pipeline (query → embed → vector DB → retrieve → context → LLM → answer)
- Video about the **agentic loop** → animate the loop diagram (model ↔ tools ↔ environment with feedback arrow)
- Video about **UI/UX** → animate a mockup of the UI being discussed (browser chrome, sidebar, buttons, content area)
- Video about **prompt engineering** → animate an actual prompt structure (system/user/assistant blocks with labels)
- Video about a **list of N things** → use the curiosity-gap pattern (show all N items, blur/redact unrevealed ones) — see the Curiosity Gap section
- Video about a **system or architecture** → animate the system design diagram (services, databases, queues, arrows)

**Forbidden as an opener:**
- A dark navy slate holding the video title in serif text
- A centered "3 Things You Should Know" / topic-name card with no diagram
- A logo or wordmark intro
- Any scene whose primary content is text restating what the speaker is about to say

If the topic does not obviously suggest a diagram, default to a labeled mockup, a flowchart of the process being described, or a side-by-side comparison of the before/after state. The opener is never a title card.

### 2. Diagrams Over Restated Text — Always

The voiceover already delivers the words. The overlay's job is to *add* information the speaker doesn't say. Bias every scene toward visuals that increase the viewer's understanding:

- **Mockup of a website / app UI** when discussing UX, products, interfaces
- **Concrete prompt examples** (with realistic system/user content, labels, token counts) when discussing prompting, context, LLM inputs
- **System design diagrams** (boxes + arrows + labels) when discussing architecture, pipelines, data flow
- **Flowcharts** when describing a sequence, decision tree, or process
- **Data visualizations** (bar charts, comparisons, sparklines) when citing numbers, benchmarks, or rankings
- **Before/after splits** when describing a transformation, fix, or improvement
- **Annotated code or config snippets** when discussing specific technical mechanics

A scene whose only visual is a line of text repeating what the speaker just said is a failure. If a scene seems to want to be a text card, redesign it as a diagram — even a simple labeled-box-and-arrow diagram beats a text card.

**Exceptions** (the only times pure text is acceptable):
- A single hero number or metric used as the focal element of a data scene
- A short pull-quote (≤6 words) used as visual punctuation, not as the scene's main content
- Labels and annotations *inside* a diagram

### 3. Fast Pacing — Visible Animation Beat Every 2–3 Seconds

Something on screen must visibly change every 2–3 seconds — either a new scene, or a new animated element entering within the current scene. Static holds longer than ~3 seconds will lose the viewer.

- **Scene length**: target ~60 frames (2s at 30fps), max ~90 frames (3s). For a 30s video that's ~12–15 scenes.
- **Within-scene animation beats**: if a scene runs longer than ~2s, stagger element entrances so a new piece reveals every 30–45 frames (1.0–1.5s) — e.g., diagram nodes appear sequentially, arrows draw in one at a time, labels fade in after their boxes.
- **No dead air**: never hold a finished, fully-revealed graphic for more than ~30 frames before cutting or adding the next beat.

This applies to the hero opener too — its construction (nodes appearing, arrows connecting, labels fading in) should itself supply 2–3 animation beats in the first 2 seconds.

## Brand Style Guide (the brand)

All overlays MUST follow these brand guidelines. This is the visual identity — do not deviate.

### Color Palette

```ts
export const COLORS = {
  // Backgrounds
  heroDark: '#0D1527',       // Deep navy — hero sections, opening slates
  lightBg: '#F4F4F2',        // Warm off-white — content sections
  cardBg: '#FFFFFF',         // Pure white — cards

  // Text
  textOnDark: '#FFFFFF',     // Primary text on dark backgrounds
  textOnLight: '#111111',    // Primary text on light backgrounds
  textMuted: '#555555',      // Secondary / supporting text
  textMeta: '#777777',       // Credentials, timestamps, labels

  // Accents
  accentGreen: '#C8F135',    // Yellow-green — underline reveals, highlight pulses (use sparingly)
  accentAmber: '#F5A623',    // Amber — star ratings, warm highlights

  // Structure
  border: '#E0E0E0',         // Dividers, card borders
};
```

### Typography

- **Serif**: EB Garamond — hero headings, large numbers, pull-quotes. Light-to-regular weight (400-500), never bold.
- **Sans**: Inter — body text, labels, data, credentials. Weights 400-800.
- Load via `@remotion/google-fonts/EBGaramond` and `@remotion/google-fonts/Inter`.

### Animation Rules

Use slow, confident easing curves — **NO spring() or bounce physics.**

```ts
import { Easing } from "remotion";
const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);      // smooth deceleration
const EASE_IN_OUT = Easing.bezier(0.4, 0, 0.2, 1);    // balanced transitions
```

- **Fade in + upward slide** (`translateY: 20px → 0`) for all element reveals
- **Staggered entrances**: 4–6 frame delay between items (NOT 10-15)
- **Underline wipe** using `accentGreen` for heading reveals (width: 0% → 100%)
- **Hero opener**: The first scene is a content-specific animated diagram (see Core Directive 1). Do NOT use a dark-navy title slate as the opener. If the hero diagram's natural background is dark, that's fine — what matters is that the dominant visual is the *diagram*, not a centered title.

**AVOID**: zoom/scale pops, spin/rotation, bounce easing, gradient washes, particle effects.

### Layout Rules

- **Cards**: White bg, `border: 1px solid #E0E0E0`, `borderRadius: 6px` max. No heavy 3px borders.
- **Spacing**: Generous — err toward more whitespace, not less. Side margins 80-100px.
- **Hierarchy**: Large serif headline → sans-serif subtitle → content grid

### Mobile Readability (CRITICAL)

These videos are watched on phones. Text must be large enough to read on a small screen.

- **Minimum font sizes**: 36px for body/labels, 56px+ for headings, 100px+ for hero numbers
- **Never use text below 32px** — if you're shrinking text to fit, you need fewer words or more scenes
- **Prefer fewer, larger elements** over many small ones
- **High contrast only** — no light gray text on white, no subtle text on busy backgrounds
- If data has many items, show the top 3-5 largest instead of cramming everything in

### Top 20% Keep-Out Zone

**Never place headers, labels, or content in the top ~200px (top 20%) of the 1080x1080 overlay frame.** This area should be clean breathing room — white space (or solid background color) only. Content starts at y≈200 or below.

Rationale: The top edge of the overlay is where the viewer's eye rests before engaging with the graphic. Clean space there looks intentional and professional. It also avoids overlap with platform UI elements (profile icons, timestamps) on TikTok/Instagram.

### Bottom Subtitle Keep-Out Zone

When the source video has **burned-in subtitles** (common with Instagram Reels), the overlay must not cover them. The caller may provide a `SUBTITLE_KEEPOUT` value — the number of pixels from the bottom of the 1080x1080 overlay that must remain clear.

**How it works:**

1. The caller detects subtitle Y-position in the original video, then calculates:
   ```
   subtitle_y_final = subtitle_y_scaled + VIDEO_OFFSET_Y
   SUBTITLE_KEEPOUT = max(0, 1080 - subtitle_y_final + 30)
   ```

2. In `theme.ts`, export the value (0 when no subtitles or subtitles are below the overlay):
   ```ts
   export const SUBTITLE_KEEPOUT = 0; // pixels from bottom of overlay to keep clear
   ```

3. In `FinalComposition.tsx`, clip the overlay div so the subtitle area shows through:
   ```tsx
   clipPath: SUBTITLE_KEEPOUT > 0
     ? `inset(0 0 ${SUBTITLE_KEEPOUT}px 0)`
     : undefined,
   ```

4. Scene components must keep all content above `1080 - SUBTITLE_KEEPOUT - 40` (40px padding above the clip edge). This is the **effective canvas bottom**.

When `SUBTITLE_KEEPOUT` is 0, behavior is unchanged — full 1080x1080 overlay. When it's, say, 240, scenes must fit within y=200 to y=800 (top keep-out + bottom keep-out).

### Overall Vibe

> Premium editorial + professional marketplace.
> Think *The Atlantic* meets *LinkedIn Learning*.
> Restrained, credentialed, trust-forward.
> No loud colors. No gradients. Confidence through simplicity.

## Prerequisites

- Python with `openai-whisper` installed (`pip install openai-whisper`)
- Node.js 18+ (for Remotion)
- ffmpeg and ffprobe (for video analysis)

## Workflow

Four phases, always in this order:

### Phase 1: Transcribe

Run the bundled transcription script:

```bash
pip install openai-whisper   # first time only
python <this-skill-path>/scripts/transcribe.py <video-file> base
```

This outputs `<filename>_transcript.json` with timestamped segments.

Store the transcript segments in `src/transcript.ts`:

```typescript
export const TRANSCRIPT_SEGMENTS = [
  { start: 0.0, end: 1.6, text: "If you're not using slash commands" },
  { start: 1.6, end: 3.1, text: "in Claude Code, you're still a rookie." },
  // ... segments from whisper output
];
```

These segments are used for timing overlay scenes to match the speaker's words.

### Phase 1.5: Research the Content

**Before designing any visuals, research the topics discussed in the video.** Use web search or your knowledge to understand the specific concepts, terminology, data points, and relationships being discussed. The overlays must be technically accurate and add visual information beyond what the speaker says.

For example, if the speaker discusses "context engineering," research what actually fills a context window (system prompts, RAG docs, few-shot examples, tool results), real token limits for popular models (200K for Claude, 128K for GPT-4o, etc.), and known problems like "lost in the middle" attention patterns.

This research also drives the **hero opener** (Core Directive 1): identify the single diagram, mockup, or system view that best captures the video's overarching idea, and plan how it animates in over the first ~2 seconds. Examples of mappings from topic → hero opener:

- "How RAG works" → animated pipeline: query → embedding → vector store → top-K retrieval → context-injected prompt → LLM → answer
- "The agentic loop" → animated loop: model node, tool node, environment node, feedback arrow drawing last
- "Why this UI feels broken" → animated mockup of the UI in question (browser frame, sidebar, header, the broken element highlighted)
- "Inside a Claude prompt" → animated prompt structure (system / user / assistant blocks with token counts and labels appearing sequentially)
- "Our infra setup" → animated system diagram (services, queues, databases, arrows drawing in)

Per Core Directive 2: every other scene also needs a non-text-restatement visual. Avoid scenes whose only content is a line of text echoing the voiceover.

### Phase 2: Design 3 Overlay Approaches

This is the creative phase. Come up with 3 visually distinct approaches for the 1080x1080 overlay animations. Each approach should have a clear visual identity that runs consistently through all its scenes.

#### Hero Opener — Required First Scene

Per Core Directive 1, the first scene is always a content-specific animated diagram. Pick the pattern that fits the video:

- **List-style video** (e.g., "3 skills", "5 mistakes") → use the **Curiosity Gap** pattern below. This *is* a valid hero opener because the full list itself is the diagram.
- **Process / pipeline video** (RAG, agentic loop, data flow) → animate the full pipeline diagram with nodes and arrows drawing in sequentially.
- **UI / product video** → animate a labeled mockup of the interface being discussed.
- **Concept / mechanism video** (how attention works, how caching works) → animate a labeled mechanism diagram (blocks, flows, state transitions).
- **Comparison video** (X vs Y) → animate a side-by-side split showing both options.

In every case, the opener animates over the first ~2 seconds with at least 2–3 visible animation beats (nodes appearing, arrows drawing, labels fading in) — never a static held title.

#### Curiosity Gap Motif (for list-style videos)

When the video discusses a list of topics (e.g., "3 skills"), use a **curiosity gap** technique:
- **Hero/hook scene**: Show all items listed, but blur/redact the ones not yet discussed. This builds viewer curiosity and retention.
- **Reveal scenes**: As each topic is introduced, unblur/reveal that item while keeping upcoming ones hidden. Previous items get dimmed or checkmarked.
- Techniques: CSS `filter: blur(8px)` on upcoming items, solid-color redaction bars that slide away, locked/unlocked module states, pyramid reveals.

**Do NOT just display the title the speaker mentions as a plain title card.** Instead, show the item being revealed within the context of the full list.

#### Approach Styles

Each of the 3 approaches is a *visual language* applied to every scene — including the hero opener and every diagram/mockup/flowchart within the video. Example approaches (vary based on content — do NOT use Terminal/CLI):

- **Editorial Infographic** — Light bg, white cards, data visualizations, metric displays, labeled diagrams
- **Dark Blueprint** — Navy bg, technical architecture diagrams, connected boxes, data flows, system designs
- **Bold Magazine** — Oversized typography wrapped around diagrams, split comparisons, hero numbers, high contrast
- **Flow Diagrams** — Process flows with boxes and arrows, gauges, architecture diagrams as the dominant motif
- **Before/After** — Split comparisons showing transformations, two-panel mockups, diff-style reveals
- **Annotated Mockup** — Simplified app/website interfaces with callouts, arrows, and labels pointing at specific UI

**AVOID**: Terminal/CLI themes (feels gimmicky). Title-card-heavy decks (violates Core Directive 1).

For each approach:
1. **Hero opener first**: design the content-specific opening diagram per Core Directive 1 and the Hero Opener section above. This is scene 1 for every approach.
2. Break the rest of the transcript into scenes targeting ~60 frames each (2s at 30fps), max ~90 frames (3s). A 30s video = ~12–15 scenes. Within any scene that runs longer than ~2s, stagger element entrances so a new visual beat appears every 30–45 frames (Core Directive 3).
3. Plan a visual for each scene — an accurate diagram, mockup, prompt example, flowchart, data viz, or comparison based on your research (Core Directive 2). A scene whose only content is a line of restated text is a failure; redesign it as a diagram.
4. Follow the brand style guide above AND the `remotion-video-creator` skill's design principles:
   - Fill ~80% of the 1080x1080 canvas (content starts at y≈200, avoiding top 20%)
   - Graphics over text (the voiceover already delivers the words)
   - Use the brand color palette (navy hero + off-white content + white cards)
   - Smooth easing animations with staggered delays (NO spring/bounce)
   - No scene headers or labels in the top 20% — keep that zone clean
   - Minimum 36px text, 56px+ headings, 100px+ hero numbers (mobile-readable)
   - Prefer fewer large elements over many small ones

#### Lecture/Link Placeholder Handling

When the speaker mentions a lecture, course, or link:
- In intermediate scenes: show a clean placeholder card with dashed border (topic name only, no literal "[LECTURE LINK]" text needed)
- In the final CTA scene: show topic cards and the CTA action — do NOT include "[LECTURE LINK]" text on the last slide

### Phase 3: Build the Remotion Project

Scaffold the project with this structure:

```
overlay/
├── public/
│   └── raw.MOV          # COPY the video here (not symlink!)
├── src/
│   ├── index.ts
│   ├── Root.tsx          # 6 compositions (3 overlay + 3 final)
│   ├── theme.ts          # Colors, font, timing constants
│   ├── transcript.ts     # Timestamped segments for scene timing
│   ├── FinalComposition.tsx   # Composites video + overlay
│   ├── v1/
│   │   ├── MainVideoV1.tsx
│   │   └── scenes/       # Scene components for version 1
│   ├── v2/
│   │   ├── MainVideoV2.tsx
│   │   └── scenes/
│   └── v3/
│       ├── MainVideoV3.tsx
│       └── scenes/
├── package.json
└── tsconfig.json
```

Read `references/compositing-patterns.md` for the exact code patterns for FinalComposition, Root, and theme. These are the compositing-specific patterns that layer the overlay on the video.

Read `references/project-scaffold.md` for package.json, tsconfig.json, and index.ts templates.

Use the `remotion-video-creator` skill for building the overlay scene components (the 1080x1080 animated content). That skill covers scene design, animation patterns, and TransitionSeries timing.

#### Critical: Video file handling

The raw video file **must be copied** (not symlinked) into the `public/` directory. Remotion's webpack bundler copies files to a temp build directory during render and does not follow symlinks, causing 404 errors.

```bash
cp /path/to/video.MOV overlay/public/raw.MOV
```

#### Determining the video offset

The speaker's head needs to appear just below the overlay area (below y=1080). To find the correct vertical offset:

1. Get video dimensions and extract a frame:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 video.MOV
ffmpeg -i video.MOV -vf "select=eq(n\,0)" -vframes 1 frame.png
```

2. Examine the frame to find the y-coordinate of the top of the speaker's hair
3. Calculate: `VIDEO_OFFSET_Y = 1080 - hairTopY`

For example, if hair top is at y=420 in the 1920px-tall frame, the offset = 1080 - 420 = 660. This shifts the video down so the hair top aligns exactly with the bottom edge of the overlay.

#### Head Placement Validation (REQUIRED)

Before committing to the `VIDEO_OFFSET_Y` value, **dispatch a subagent to validate the head placement**. This catches errors before they propagate into all 3 renders.

1. After calculating `VIDEO_OFFSET_Y`, generate a **composited preview frame** using ffmpeg:

```bash
# Extract a representative frame from the raw video (frame 30 = ~1 second in)
ffmpeg -i video.MOV -vf "select=eq(n\,30)" -vframes 1 raw_frame.png

# Create a blank 1080x1920 canvas, place the video frame at the calculated offset,
# and draw a red guide line at y=1080 (the overlay boundary)
ffmpeg -f lavfi -i "color=black:s=1080x1920:d=1" \
  -i raw_frame.png \
  -filter_complex "[0:v][1:v]overlay=0:${VIDEO_OFFSET_Y},drawbox=y=1080:w=1080:h=2:color=red:t=fill[out]" \
  -map "[out]" -frames:v 1 head_placement_check.png
```

2. **Dispatch a subagent** (using the Agent tool) to review the generated `head_placement_check.png`. The subagent prompt should be:

> Review the image `head_placement_check.png`. This is a 1080x1920 composited preview frame for a vertical video overlay pipeline.
>
> The RED horizontal line at y=1080 marks the boundary between the overlay zone (top half) and the speaker zone (bottom half).
>
> Validate ALL of the following:
> - **Head clearance**: The top of the speaker's hair should be JUST BELOW the red line (within ~20px). If the hair is significantly above the line, the overlay will cover the speaker's head. If it's too far below, there will be a visible gap/black bar.
> - **Head centering**: The speaker's head should be roughly horizontally centered in the frame. Flag if the head is noticeably off-center.
> - **Head cropping**: The speaker's chin and shoulders should be visible — the head should NOT be cropped at the bottom of the frame.
> - **Overall composition**: Does the placement look natural? Would a viewer see a clean transition from overlay graphics to the speaker?
>
> Respond with:
> - **PASS** if placement looks correct, with a brief confirmation
> - **FAIL** with specific issues and a recommended adjustment (e.g., "hair is ~60px above the red line, increase VIDEO_OFFSET_Y by ~60")

3. **If the subagent returns FAIL**: Adjust `VIDEO_OFFSET_Y` per its recommendation, regenerate the preview, and re-validate. Repeat until PASS.

4. **If the subagent returns PASS**: Proceed to build the Remotion project with the validated offset value.

**Do not skip this step.** An incorrect offset ruins all 3 final renders and wastes significant render time.

#### Building overlay compositions

Use the `remotion-video-creator` skill to write each version's scene components. Follow its Phase 2 (Design) and Phase 3 (Build) workflows for the 1080x1080 overlay content.

Each version needs:
- A `MainVideoVN.tsx` wrapping scenes in `TransitionSeries` with 10-frame fade transitions
- Individual scene components in `vN/scenes/`
- Shared timing constants from `theme.ts`

#### Root.tsx composition structure

Register 6 compositions:
- 3 overlay-only previews (1080x1080) — for previewing overlays in isolation
- 3 final renders (1080x1920) — the complete composited video with overlay

### Phase 4: Render

Preview in Remotion studio first to verify timing and positioning, then render all 3:

```bash
npx remotion render src/index.ts FinalV1 out/final_v1.mp4 --codec h264 --crf 18
npx remotion render src/index.ts FinalV2 out/final_v2.mp4 --codec h264 --crf 18
npx remotion render src/index.ts FinalV3 out/final_v3.mp4 --codec h264 --crf 18
```

CRF 18 gives high visual quality. The h264 codec ensures compatibility with all social platforms.

---

## Reference Files

- **[references/compositing-patterns.md](references/compositing-patterns.md)** — Complete code for FinalComposition.tsx, transcript.ts format, theme.ts, and Root.tsx with all 6 compositions. Read this when building the compositing layer.
- **[references/project-scaffold.md](references/project-scaffold.md)** — package.json, tsconfig.json, and index.ts templates. Read when setting up the project.
- **remotion-video-creator skill** — Design principles, scene planning, and animation patterns for the 1080x1080 overlay content. Always consult this for the overlay scenes.
- **remotion-best-practices skill** — Remotion API reference for advanced features.
