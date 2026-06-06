---
name: MorphFlow
colors:
  surface: '#fdf8f8'
  surface-dim: '#ddd9d8'
  surface-bright: '#fdf8f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f7f3f2'
  surface-container: '#f1edec'
  surface-container-high: '#ebe7e6'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#444748'
  inverse-surface: '#313030'
  inverse-on-surface: '#f4f0ef'
  outline: '#747878'
  outline-variant: '#c4c7c7'
  surface-tint: '#5f5e5e'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1c1b1b'
  on-primary-container: '#858383'
  inverse-primary: '#c8c6c5'
  secondary: '#5e5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e1dfdf'
  on-secondary-container: '#626262'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#1d1b1a'
  on-tertiary-container: '#868381'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e5e2e1'
  primary-fixed-dim: '#c8c6c5'
  on-primary-fixed: '#1c1b1b'
  on-primary-fixed-variant: '#474646'
  secondary-fixed: '#e4e2e2'
  secondary-fixed-dim: '#c7c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#464747'
  tertiary-fixed: '#e6e1df'
  tertiary-fixed-dim: '#cac6c3'
  on-tertiary-fixed: '#1d1b1a'
  on-tertiary-fixed-variant: '#484645'
  background: '#fdf8f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
typography:
  display:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label-md:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.02em
  mono-sm:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-padding-desktop: 48px
  container-padding-mobile: 20px
  gutter: 24px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
  section-gap: 64px
---

## Brand & Style
The design system is built on the principles of **High-End Minimalism** and **Functional Sophistication**. It targets a professional audience of creators, developers, and product teams who value speed and clarity. The aesthetic draws heavily from modern technical SaaS leaders, prioritizing intent over decoration.

The emotional goal is to evoke a sense of **calm authority** and **limitless potential**. By utilizing a monochromatic palette and significant whitespace, the UI recedes into the background, allowing the user's AI-generated video content to remain the focal point. The style is strictly "Modern SaaS," characterized by sharp execution, meticulous alignment, and a total absence of unnecessary visual noise.

## Colors
The palette is intentionally restrained to maintain a premium, editorial feel. 
- **Primary Text & Accent (#111111):** Used for headlines, primary buttons, and active states. It represents the "ink" of the system.
- **Secondary Text (#666666):** Used for descriptions, labels, and metadata to create a clear visual hierarchy.
- **Surface (#FAFAFA):** A subtle off-white used for secondary containers, sidebar backgrounds, and input fields to differentiate from the pure white canvas.
- **Border (#EAEAEA):** The structural backbone of the design. Used for subtle containment and separation without adding visual weight.

## Typography
We use **Hanken Grotesk** for its sharp, contemporary geometry and high legibility. It provides a "tech-forward" feel that remains approachable. For technical data and labels, **Geist** provides a precise, developer-centric rhythm.

The hierarchy is driven by significant scale differences and weight. Large headlines use tight tracking and leading to feel like modern editorial titles, while body text uses generous leading (1.6x) to ensure maximum readability during long creative sessions.

## Layout & Spacing
The spacing philosophy is "Generous and Intentional." We use a 4px base unit. 
- **Desktop:** 12-column fluid grid with a max-width of 1440px. Large margins (48px) create a frame-like effect for the workspace.
- **Reflow:** On tablet, gutters remain 24px but margins reduce to 32px. On mobile, the layout shifts to a single column with 20px side margins.
- **Negative Space:** Do not fear empty space. Large gaps (64px+) should be used to separate primary functional areas (e.g., Timeline vs. Properties Panel).

## Elevation & Depth
This design system avoids traditional heavy drop shadows. Depth is achieved through:
1.  **Tonal layering:** Placing #FAFAFA surfaces on #FFFFFF backgrounds to indicate depth.
2.  **Ultra-subtle borders:** #EAEAEA outlines are the primary tool for defining object boundaries.
3.  **The "Ambient Lift":** Only floating elements (dropdowns, modals) receive a shadow. These shadows should be extremely diffused: `0 10px 30px rgba(0,0,0,0.04)`.
4.  **Glassmorphism:** Navigation bars and sticky headers should use a `backdrop-filter: blur(12px)` with a semi-transparent white background (`rgba(255,255,255,0.8)`) to maintain context while scrolling.

## Shapes
A signature of this design system is the use of **Large Border Radii**. This softens the technical nature of AI video generation, making the platform feel friendly and high-end. 
- **Small elements (Buttons/Inputs):** 8px (standard rounded).
- **Medium elements (Cards/Sidebars):** 16px (rounded-lg).
- **Large elements (Video Player/Main Containers):** 24px (rounded-xl).
- **Interactive States:** Focus states should use a 2px offset with a solid 2px #111111 border to ensure accessibility without breaking the minimalist aesthetic.

## Components
- **Buttons:** Primary buttons are solid #111111 with white text. Secondary buttons use a white background with a #EAEAEA border. Hover states involve a subtle opacity shift or a slight "lift" using the ambient shadow.
- **Inputs:** Use the #FAFAFA surface color. Labels sit above the field in `label-md` typography. Borders only appear on focus.
- **Cards:** No shadows by default. Use a 1px #EAEAEA border and 16px-24px corner radius. Content inside should have at least 24px of internal padding.
- **Chips/Tags:** Small, pill-shaped elements with #FAFAFA backgrounds and `label-md` text. Used for status indicators (e.g., "Rendering", "Draft").
- **Lists:** Clean rows separated by 1px #EAEAEA horizontal lines. Use generous vertical padding (16px) for each list item to maintain the "premium" feel.
- **Video Timeline:** A custom component using #111111 for the playhead and #EAEAEA for the track background. Keyframes should be simple geometric shapes (diamonds or circles).