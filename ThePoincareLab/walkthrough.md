# The Poincaré Lab — Walkthrough

A cinematic, real-time interactive simulation of the **three-body gravitational problem**, built as a React + Vite web application.

---

## How to Run

### Prerequisites

- Node.js ≥ 18
- npm

### Start the dev server

```bash
cd ThePoincareLab
npm install       # first time only
npm run dev
```

Then open **http://localhost:5173** (or 5174 if that port is taken) in your browser.

![alt text](poincare-ui.png)

---

## What You'll See

### 🌌 Hero — The Simulation (first screen)

The entire background is a **live physics simulation** of three stars pulling on each other via gravity, rendered frame-by-frame on an HTML5 Canvas.

| Element | Location | Description |
|---|---|---|
| Three glowing suns | Center | Cyan · Violet · White orbs with bloom trails |
| Title | Bottom-left | "THE POINCARÉ LAB" |
| Telemetry | Top-right | Shows integrator status and timestep |
| Control panel | Bottom-right | Mass sliders + time controls |

### 🎛️ Control Panel (bottom-right of first screen)

**Mass Constructor** — three sliders, one per star:
- Drag **left** → lower mass → weaker gravity → slower, wider orbits
- Drag **right** → higher mass → stronger gravity → tightly wound, faster chaos

**Temporal Governor** — speeds up or slows down the simulation (0.1× to 5×)

**RESET TRACES** — clears the glowing trail paths

> All changes take effect **instantly** — the canvas re-renders on every animation frame.

---

## Scroll Down — The Physics Archive

Three full-screen cards that pin as you scroll, each explaining one law:

| Card | Topic |
|---|---|
| ARCHIVE 01 | **Newton's Law of Gravitation** — F = G·m₁m₂/r² |
| ARCHIVE 02 | **The Butterfly Effect** — exponential divergence from tiny perturbations |
| ARCHIVE 03 | **Periodic Solutions** — the "Figure-8" choreography and other stable orbits |

---

## How the Physics Works

The simulation uses a **4th-order Runge-Kutta (RK4)** integrator running in a `requestAnimationFrame` loop:

1. For each frame (~16 ms), the loop runs **8 sub-steps** for numerical stability
2. Each sub-step computes the **gravitational acceleration** between all 3 body pairs: `a = G·m/r²`
3. A **softening parameter** prevents infinite forces when bodies pass very close
4. The **camera follows the center of mass** so the action stays centered on screen

The physics state lives in plain `useRef` (not React state) so mass changes and physics updates never cause React re-renders — keeping it at **60 FPS** even during slider interaction.

---

## Project Structure

```
ThePoincareLab/
├── src/
│   ├── App.jsx                    # Root layout, initial conditions
│   ├── main.jsx                   # React entry point
│   ├── index.css                  # Global base styles
│   ├── hooks/
│   │   └── useThreeBody.js        # RK4 physics engine
│   └── components/
│       ├── SimulationCanvas.jsx   # Canvas renderer + animation loop
│       ├── HeroOverlay.jsx        # Title, telemetry overlay
│       ├── Laboratory.jsx         # Mass + time dilation controls
│       └── LawsArchive.jsx        # GSAP scroll-stacking narrative
├── z-tech-stack.md                # Design & architecture decisions
└── walkthrough.md                 # This file
```

---

## Initial Conditions (Chaotic Triple-Sun)

```
Positions:  [-2, 0.5], [2, -0.5], [0, 2]    (visual units)
Velocities: [0, 0.6],  [0, -0.6], [-0.6, 0]
Masses:     1.0, 1.0, 1.0                    (equal mass chaos)
```

The slightly asymmetric positions guarantee the system never settles into a stable orbit — it is **chaotic by design**.
