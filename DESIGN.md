---
title: Nexus AI Resume Builder
version: 1.0.0
tokens:
  colors:
    background:
      dark: "#07070A"
      gradient_start: "#0F1219"
      gradient_end: "#07070A"
      panel: "rgba(18, 18, 22, 0.7)"
    accents:
      indigo: "#818CF8"
      purple: "#C084FC"
      cyan: "#22D3EE"
      emerald: "#34D399"
      rose: "#FB7185"
    text:
      primary: "#F8FAFC"
      secondary: "#94A3B8"
      muted: "#64748B"
    border:
      glass: "rgba(255, 255, 255, 0.08)"
      highlight: "rgba(255, 255, 255, 0.1)"
  typography:
    families:
      sans: "'Inter', system-ui, sans-serif"
      heading: "'Sora', system-ui, sans-serif"
    weights:
      light: 300
      regular: 400
      medium: 500
      semibold: 600
      bold: 700
    letter_spacing:
      heading: "-0.02em"
  radii:
    none: "0"
    md: "12px"
    lg: "16px"
    xl: "20px"
    luxury: "28px"
    full: "100px"
  elevation:
    glass: "0 8px 32px 0 rgba(0, 0, 0, 0.6)"
    hover: "0 24px 48px rgba(0, 0, 0, 0.5)"
    luxury: "0 40px 60px -15px rgba(0,0,0,0.8)"
  motion:
    easings:
      out: "cubic-bezier(0.16, 1, 0.3, 1)"
      in_out: "cubic-bezier(0.22, 1, 0.36, 1)"
    durations:
      micro: "220ms"
      soft: "400ms"
      entrance: "700ms"
      page: "800ms"
---

# Design System: Nexus AI

Nexus AI is a premium, high-fidelity resume intelligence platform. The design language, dubbed **"Atmospheric Glass,"** balances deep futuristic tones with organic gradients and sophisticated glassmorphism. It is designed to feel high-tech, trustworthy, and incredibly smooth.

## 1. Visual Identity & Atmosphere

The aesthetic is rooted in **Dark Mode Excellence**. Rather than using flat blacks, it uses a deep charcoal and navy foundation (`#07070A`) with fixed ambient orbs that drift slowly in the background. These orbs (Indigo, Purple, and Emerald) create a sense of depth and life without distracting the user.

- **Vibe**: Luxury, Intelligent, Precise, Cinematic.
- **Glassmorphism**: Panels use high blur values (20px+) and very subtle borders to feel like floating physical glass.
- **Gradients**: Used sparingly but impactfully on text and primary actions to guide the eye and signify premium AI features.

## 2. Typography

The system uses a two-font strategy:
- **Sora**: The heading font. Its wide, geometric characters feel modern and "designed." It is always used with tight letter-spacing (`-0.02em`) to maintain a professional, high-end look.
- **Inter**: The workhorse sans-serif for body text and inputs, ensuring maximum legibility across all data-dense areas.

## 3. Component Styling

### 3.1 Nexus Cards
Cards are the primary container unit. They feature:
- **Geometry**: Generously rounded corners (20px to 28px).
- **Interactions**: On hover, cards lift vertically (`-4px` to `-8px`) and their shadow depth doubles, creating a physical "rising" effect.
- **Material**: Subtle internal top-left gradients to simulate light catching the edge of the glass.

### 3.2 Premium Inputs
Inputs are integrated into the glass aesthetic:
- **Default State**: Dark, nearly transparent backgrounds with fine borders.
- **Focus State**: Borders glow with **Accent Emerald**, accompanied by a soft spread shadow to indicate active focus.
- **Floating Labels**: Labels shift upward and scale down on focus, keeping the interface clean.

### 3.3 Buttons & Pills
- **Btn-Premium**: A pill-shaped button with a subtle translucent fill and blur.
- **Btn-Primary-Glow**: The "Hero" button, using a vibrant Indigo-Purple gradient and a persistent soft outer glow to signify the primary path.
- **Status Pills**: Used for confidence scores and ATS rankings, utilizing the semantic colors (Emerald for success, Rose for danger, Amber for warning).

## 4. Motion & Interactivity

Motion is not an afterthought; it is a core token. 
- **The "Nexus Ease"**: Most transitions use `cubic-bezier(0.16, 1, 0.3, 1)`, a timing function that starts fast and ends with a long, smooth deceleration.
- **Staggered Entrances**: New screens and list items do not just appear; they fade and slide up in a staggered sequence (60ms intervals), giving a sense of the system "assembling" itself.
- **Pulse Indicators**: Vital system states (like an active AI coach) use a soft breathing pulse animation to feel "alive."

## 5. Layout Principles

- **Bento Grids**: Complex data (like resume metrics) is organized into a modular bento grid, allowing for responsive reshuffling while maintaining a structured, modern feel.
- **Generous Whitespace**: High-end design requires room to breathe. Margins and paddings follow a strict scale, often using large bottom margins (`mb-6`, `mb-7`) to separate major conceptual sections.
- **Z-Index Layering**: Navigation is the top-most layer with a high-blur "Glass Nav" effect, ensuring content scrolls beautifully underneath it.
