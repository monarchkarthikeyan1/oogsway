# UI/UX & Information Architecture Specification — The Lenny Growth Assistant

## 1. Design Aesthetics & Visual Tokens

The user interface of "The Lenny Growth Assistant" is built to deliver a state-of-the-art, premium experience inspired by Claude Artifacts, Linear, and modern glassmorphic web design.

```
       Visual Aesthetic Palette
┌──────────────────────────────────────┐
│ Background: #090d16 (Deep Slate Dark) │
│ Glass Panel: rgba(15, 23, 42, 0.75)  │
│ Accent Cyan: #38bdf8 (Sky Blue Glow)  │
│ Accent Emerald: #34d399 (Growth Green)│
│ Accent Purple: #a855f7 (PLG Purple)  │
└──────────────────────────────────────┘
```

### Key Design Tokens:
- **Typography**: Primary font family `Inter` (sans-serif) for high readability; `JetBrains Mono` for citations, code, and timestamps.
- **Glassmorphism**: Translucent panels (`backdrop-filter: blur(16px)`) with subtle 1px border highlights (`rgba(255,255,255,0.08)`).
- **Micro-Animations**: Hover state elevation, glowing borders on action pills, smooth slide-over animation for the Artifact Viewer drawer.

---

## 2. Information Architecture & Layout Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              HEADER (Navbar)                                │
│ Logo | App Title | Active Provider Pill (Ollama/Claude) | Security | Settings │
├─────────────┬───────────────────────────────────────────────┬───────────────┤
│   SIDEBAR   │                 CHAT WINDOW                   │   ARTIFACT    │
│             │                                               │    VIEWER     │
│ Chat        │ [Bot Message with Citations [1] [2]]          │ (Claude-Style │
│ History     │                                               │  Split Pane)  │
│             │ ┌───────────────────────────────────────────┐ │               │
│ Growth      │ │ 🎨 Interactive Artifact Preview Card       │ │  Preview      │
│ Skills:     │ │ Click to open in Side Panel               │ │  Code         │
│ • Ship 30   │ └───────────────────────────────────────────┘ │  Copy         │
│ • HTML Art  │                                               │  Download     │
│ • PLG Loops │ ┌───────────────────────────────────────────┐ │               │
│             │ │ CHAT INPUT: Mode Pills | Send Button      │ │               │
│ Transcript  │ └───────────────────────────────────────────┘ │               │
│ Stats Index │                                               │               │
└─────────────┴───────────────────────────────────────────────┴───────────────┘
```

---

## 3. Key Interaction States

1. **Idle / Empty State**:
   - Displays brand logo, introduction, and quick-start skill prompt cards.
2. **Streaming / Synthesis State**:
   - Displays pulsing animated bot badge and real-time status banner (*"Searching transcripts and synthesizing grounded response..."*).
3. **Citation Inspector State**:
   - Clicking inline markers `[1]` opens an overlay drawer with the exact guest quote, episode title, timestamp, and link.
4. **Artifact Preview State**:
   - Clicking an artifact card opens the right 50% split pane, presenting the rendered HTML preview or Markdown source code.
5. **Model Provider Toggle State**:
   - Modal dialog listing Ollama, Anthropic Claude, and OpenAI with real-time health indicator dots.

---

## 4. Accessibility & Responsive Design

- **Color Contrast**: All text elements meet WCAG AA contrast standards (> 4.5:1 ratio against slate backgrounds).
- **Keyboard Navigation**: Chat input supports standard `Enter` to submit and `Shift+Enter` for newlines.
- **Responsive Layout**: On mobile screens, the side sidebar collapses and the Artifact Viewer transforms into a full-screen modal drawer.
