import React, { useState } from 'react';
import { useThreeBody } from './hooks/useThreeBody';
import { SimulationCanvas } from './components/SimulationCanvas';
import { HeroOverlay } from './components/HeroOverlay';
import { Laboratory } from './components/Laboratory';
import { LawsArchive } from './components/LawsArchive';

// Chaotic Triple-Sun initial state (visual units, G=0.5)
const INIT_POSITIONS = [
  [-2.0, 0.5, 0],
  [2.0, -0.5, 0],
  [0.0, 2.0, 0],
];
const INIT_VELOCITIES = [
  [0.0, 0.6, 0],
  [0.0, -0.6, 0],
  [-0.6, 0.0, 0],
];
const INIT_MASSES = [1.0, 1.0, 1.0];

export default function App() {
  const [timeDilation, setTimeDilation] = useState(1.0);
  const engine = useThreeBody(INIT_POSITIONS, INIT_VELOCITIES, INIT_MASSES);

  return (
    <div style={{ background: '#05070A', minHeight: '100vh' }}>

      {/* Fixed canvas lives behind everything */}
      <SimulationCanvas engine={engine} timeDilation={timeDilation} />

      {/* Hero section — full screen with overlay and control panel */}
      <div style={{ position: 'relative', height: '100vh', width: '100%', overflow: 'hidden' }}>
        <HeroOverlay />
        <Laboratory engine={engine} onTimeDilation={setTimeDilation} />
      </div>

      {/* Scrollable physics narrative below the fold */}
      <LawsArchive />
    </div>
  );
}
