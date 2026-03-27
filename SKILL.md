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

# Video Overlay Pipeline

Takes a vertical (9:16) talking-head video, creates 3 different animated overlay variations synced to the transcript, composites each overlay on top of the original video, and renders 3 final TikTok-ready MP4s. No captions are added.

The output is 3 complete 1080x1920 videos where:
- **Top half** (1080x1080): Animated overlay graphics following the design system below
- **Bottom half**: The speaker's head/shoulders from the original video, shifted so head sits just below the overlay

## Design System

All overlays should feel like a polished VC pitch deck — clean, authoritative, and data-forward. The aesthetic is premium and minimal, not flashy.

### Color Palette

```ts
export const COLORS = {
  // Backgrounds
  heroDark: '#1A1A2E',       // Deep charcoal-navy — hero sections, opening slates
  lightBg: '#FAFAFA',        // Clean off-white — content sections
  cardBg: '#FFFFFF',         // Pure white — cards

  // Text
  textOnDark: '#FFFFFF',     // Primary text on dark backgrounds
  textOnLight: '#1A1A1A',    // Primary text on light backgrounds
  textMuted: '#6B7280',      // Secondary / supporting text
  textMeta: '#9CA3AF',       // Credentials, timestamps, labels

  // Accents
  accentBlue: '#3B82F6',     // Primary accent — highlights, underlines, key metrics
  accentTeal: '#14B8A6',     // Secondary accent — success states, positive data

  // Structure
  border: '#E5E7EB',         // Dividers, card borders
};
```

### Typography

- **Heading**: DM Sans — headings, large numbers, key metrics. Weights 500-700.
- **Body**: Inter — body text, labels, data, credentials. Weights 400-700.
- Load via `@remotion/google-fonts/DMSans` and `@remotion/google-fonts/Inter`.

### Animation Rules

Use slow, confident easing curves — **NO spring() or bounce physics.**

```ts
import { Easing } from "remotion";
const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);      // smooth deceleration
const EASE_IN_OUT = Easing.bezier(0.4, 0, 0.2, 1);    // balanced transitions
```

- **Fade in + upward slide** (`translateY: 20px → 0`) for all element reveals
- **Staggered entrances**: 4–6 frame delay between items (NOT 10-15)
- **Underline wipe** using `accentBlue` for heading reveals (width: 0% → 100%)
- **Opening slate**: Start on dark background, hold 20-30 frames, then crossfade to light content

**AVOID**: zoom/scale pops, spin/rotation, bounce easing, gradient washes, particle effects.

### Layout Rules

- **Cards**: White bg, `border: 1px solid #E5E7EB`, `borderRadius: 8px`. No heavy borders.
- **Spacing**: Generous — err toward more whitespace, not less. Side margins 80-100px.
- **Hierarchy**: Large bold heading → lighter subtitle → content grid

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

### Overall Vibe

> Clean, authoritative, investor-grade.
> Think Sequoia pitch deck meets *The Economist* data visualization.
> Confident whitespace. Sharp data. No decoration for decoration's sake.
> Every element earns its place on screen.

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

**Do NOT create generic title cards that just restate what the speaker says.** The graphics should teach or illustrate — showing diagrams, data, comparisons, or visual metaphors that complement the voiceover.

### Phase 2: Design 3 Overlay Approaches

This is the creative phase. Come up with 3 visually distinct approaches for the 1080x1080 overlay animations. Each approach should have a clear visual identity that runs consistently through all its scenes.

#### Curiosity Gap Motif (REQUIRED)

When the video discusses a list of topics (e.g., "3 skills"), use a **curiosity gap** technique in the hook and reveal scenes:
- **Hook scene**: Show all items listed, but blur/redact the ones not yet discussed. This builds viewer curiosity and retention.
- **Reveal scenes**: As each topic is introduced, unblur/reveal that item while keeping upcoming ones hidden. Previous items get dimmed or checkmarked.
- Techniques: CSS `filter: blur(8px)` on upcoming items, solid-color redaction bars that slide away, locked/unlocked module states, pyramid reveals.

**Do NOT just display the title the speaker mentions as a plain title card.** Instead, show the item being revealed within the context of the full list.

#### Approach Styles

Example approaches (vary based on content — do NOT use Terminal/CLI):
- **Editorial Infographic** — Light bg, white cards, data visualizations, metric displays
- **Dark Blueprint** — Dark bg, technical architecture diagrams, connected boxes, data flows
- **Bold Magazine** — Oversized typography, split comparisons, hero numbers, high contrast
- **Flow Diagrams** — Process flows with boxes and arrows, gauges, architecture diagrams
- **Before/After** — Split comparisons showing transformations
- **Mockup UI** — Simplified app interfaces (dashboards, search bars, routing diagrams)

**AVOID**: Terminal/CLI themes (feels gimmicky).

For each approach:
1. Break the transcript into scenes with a **scene change every ~2 seconds** for fast, engaging pacing (e.g., a 30s video = ~15 scenes). Each scene should be a distinct visual beat — don't hold any single graphic too long
2. Plan a visual for each scene — an accurate diagram, data visualization, or visual metaphor based on your research
3. Follow the design system above AND the `remotion-video-creator` skill's design principles:
   - Fill ~80% of the 1080x1080 canvas (content starts at y≈200, avoiding top 20%)
   - Graphics over text (the voiceover already delivers the words)
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
