# The Poincaré Lab - Architecture & Aesthetics

## Core Directives

**Aesthetics Preset:** Preset D — "Cosmic Entropy" (The Gold Standard)
**Initial Orbital State:** Chaotic Triple-Sun
**Primary Interactive Goal:** Modify Mass

## Visual Language (Cosmic Entropy)
*   **Palette:**
    *   Deep Space Void: `#05070A`
    *   Pulsar Cyan: `#00F0FF`
    *   Event Horizon Violet: `#1A0B2E`
    *   Text/Accents: `#E8E4DD` (Paper) / `#FFFFFF` (Supernova White)
*   **Typography:**
    *   Headers / Display: "IBM Plex Sans" (Clean, scientific authority)
    *   Data / Telemetry: "IBM Plex Mono" (Tabular, precise)
*   **Texture:**
    *   Inline SVG noise filter (0.04 opacity) applied globally to simulate physical hardware screens.
*   **Hero Visuals:**
    *   High-fidelity nebula-like bloom renders on the bodies.
    *   Fading "ghost" trails for orbital paths.
    *   Telemetry grid overlays.

## Tech Stack
*   **Framework:** React 19 (via Vite)
*   **Styling:** Tailwind CSS + Vanilla CSS (for complex grain/bloom effects)
*   **Animation/Interaction:** GSAP 3 (ScrollTrigger for stacking, general tweening) + Framer Motion (magnetic UI)
*   **Physics Engine:** Custom standard JavaScript implementation of 4th-order Runge-Kutta (RK4) or Verlet Integration running in a `requestAnimationFrame` loop decoupled from React state to prevent render lag.
*   **Rendering:** HTML5 Canvas API (Full-screen background behind the Hero)
*   **Icons:** Lucide React

## Component Architecture

1.  **`App.jsx` (The Global State):**
    *   Mounts the Canvas, UI overlays, and manages high-level logic.

2.  **`SimulationCanvas.jsx` (The Engine):**
    *   Houses the `requestAnimationFrame` loop.
    *   Executes the RK4/Verlet integration.
    *   Draws the glowing orbs, trails, and handles canvas resizing.

3.  **`HeroOverlay.jsx` (The Event Horizon):**
    *   Heavy radial gradient (`bg-radial-at-b`).
    *   Telemetry Data (top-right).
    *   Title/BrandCTA (bottom-left).

4.  **`Laboratory.jsx` (System Parameter Modules):**
    *   **Card 1: Mass Constructor (Primary Focus):** Three vertical/horizontal high-precision sliders to live-update the mass of the three suns.
    *   **(Optional/Secondary) Card 2 & 3:** Vector input and Time Dilation, subordinate to Mass manipulation.

5.  **`LawsArchive.jsx` (GSAP Scroll Stacking):**
    *   Full-screen pinning cards explaining:
        1.  The Law of Gravitation (LaTeX rendering).
        2.  The Butterfly Effect.
        3.  The Chaotic Nature of the Triple-Sun system.

## The Physics Model (JavaScript translation of Python `solve_ivp`)
*   We will port the core `three_body_equations` from the existing Python backend into a pure JavaScript class or custom hook (`useThreeBody`).
*   **Performance Note:** To achieve 60FPS fluid interactivity while modifying mass, the integration steps must be carefully tuned (e.g., fixed time steps with multiple sub-steps per frame) and drawn directly to the canvas context, bypassing React's render cycle for the bodies themselves.
