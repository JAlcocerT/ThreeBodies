import React, { useState } from 'react';

const BODY_COLORS = ['#00F0FF', '#BF5FFF', '#FFFFFF'];
const BODY_NAMES = ['Pulsar Alpha', 'Violet Beta', 'Nova Gamma'];

const sectionStyle = {
    minHeight: '100vh',
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#05070A',
    borderTop: '1px solid rgba(0,240,255,0.12)',
    position: 'relative',
    zIndex: 10,
    padding: '4rem 2rem',
    boxSizing: 'border-box',
};

const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '1.25rem',
    width: '100%',
    maxWidth: '1100px',
};

const cardStyle = {
    background: 'rgba(26,11,46,0.5)',
    border: '1px solid rgba(0,240,255,0.15)',
    borderRadius: '10px',
    padding: '1.5rem',
    backdropFilter: 'blur(12px)',
};

const labelStyle = {
    fontFamily: '"IBM Plex Mono", monospace',
    fontSize: '0.68rem',
    color: 'rgba(232,228,221,0.5)',
    letterSpacing: '0.12em',
    textTransform: 'uppercase',
    marginBottom: '0.3rem',
    display: 'block',
};

const valueStyle = {
    fontFamily: '"IBM Plex Mono", monospace',
    fontSize: '0.85rem',
    marginBottom: '0.35rem',
};

const Slider = ({ label, value, min, max, step, color, onChange }) => (
    <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
            <span style={{ ...labelStyle, marginBottom: 0 }}>{label}</span>
            <span style={{ ...valueStyle, color }}>{parseFloat(value).toFixed(2)}</span>
        </div>
        <input
            type="range" min={min} max={max} step={step} value={value}
            onChange={e => onChange(parseFloat(e.target.value))}
            style={{ width: '100%', accentColor: color, cursor: 'pointer', marginTop: '0.3rem' }}
        />
    </div>
);

export const Playground = ({ onRelaunch }) => {
    // Initial velocity x and y per body
    const [vx, setVx] = useState([0.0, 0.0, -0.6]);
    const [vy, setVy] = useState([0.6, -0.6, 0.0]);
    // Positions offset (x only for simplicity)
    const [px, setPx] = useState([-2.0, 2.0, 0.0]);
    const [py, setPy] = useState([0.5, -0.5, 2.0]);

    const handleVx = (i, v) => { const next = [...vx]; next[i] = v; setVx(next); };
    const handleVy = (i, v) => { const next = [...vy]; next[i] = v; setVy(next); };
    const handlePx = (i, v) => { const next = [...px]; next[i] = v; setPx(next); };
    const handlePy = (i, v) => { const next = [...py]; next[i] = v; setPy(next); };

    const handleLaunch = () => {
        const positions = px.map((x, i) => [x, py[i], 0]);
        const velocities = vx.map((x, i) => [x, vy[i], 0]);
        onRelaunch(positions, velocities);
    };

    const handleRandom = () => {
        const rand = (lo, hi) => lo + Math.random() * (hi - lo);
        const newPx = [rand(-3, -1), rand(1, 3), rand(-1, 1)];
        const newPy = [rand(-1, 1), rand(-1, 1), rand(1, 3)];
        const newVx = [rand(-1, 1), rand(-1, 1), rand(-1, 1)];
        const newVy = [rand(-1, 1), rand(-1, 1), rand(-1, 1)];
        setPx(newPx); setPy(newPy); setVx(newVx); setVy(newVy);
        onRelaunch(
            newPx.map((x, i) => [x, newPy[i], 0]),
            newVx.map((x, i) => [x, newVy[i], 0])
        );
    };

    return (
        <section style={sectionStyle}>
            <div style={{ width: '100%', maxWidth: '1100px' }}>
                {/* Header */}
                <div style={{ marginBottom: '3rem', textAlign: 'center' }}>
                    <div style={{ fontFamily: '"IBM Plex Mono", monospace', color: '#00F0FF', fontSize: '0.65rem', letterSpacing: '0.3em', marginBottom: '0.75rem' }}>
                        TERMINAL // INITIAL CONDITIONS
                    </div>
                    <h2 style={{ fontFamily: '"IBM Plex Sans", sans-serif', fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 700, color: '#FFFFFF', margin: 0, textShadow: '0 0 30px rgba(0,240,255,0.3)' }}>
                        The Playground
                    </h2>
                    <p style={{ fontFamily: '"IBM Plex Sans", sans-serif', color: 'rgba(232,228,221,0.6)', marginTop: '0.75rem', fontSize: '1rem', maxWidth: '500px', margin: '0.75rem auto 0' }}>
                        Set the initial position and velocity of each body, then relaunch the simulation to explore new orbits.
                    </p>
                </div>

                {/* Body cards */}
                <div style={gridStyle}>
                    {[0, 1, 2].map(i => (
                        <div key={i} style={{ ...cardStyle, borderColor: BODY_COLORS[i] + '33' }}>
                            <div style={{ fontFamily: '"IBM Plex Mono", monospace', color: BODY_COLORS[i], fontSize: '0.7rem', letterSpacing: '0.2em', marginBottom: '1.25rem' }}>
                                ◉ {BODY_NAMES[i]}
                            </div>

                            <div style={{ fontFamily: '"IBM Plex Mono", monospace', color: 'rgba(232,228,221,0.4)', fontSize: '0.6rem', letterSpacing: '0.15em', marginBottom: '0.75rem' }}>
                                POSITION
                            </div>
                            <Slider label="X" value={px[i]} min={-5} max={5} step={0.1} color={BODY_COLORS[i]} onChange={v => handlePx(i, v)} />
                            <Slider label="Y" value={py[i]} min={-5} max={5} step={0.1} color={BODY_COLORS[i]} onChange={v => handlePy(i, v)} />

                            <div style={{ fontFamily: '"IBM Plex Mono", monospace', color: 'rgba(232,228,221,0.4)', fontSize: '0.6rem', letterSpacing: '0.15em', margin: '0.75rem 0' }}>
                                VELOCITY
                            </div>
                            <Slider label="Vx" value={vx[i]} min={-3} max={3} step={0.05} color={BODY_COLORS[i]} onChange={v => handleVx(i, v)} />
                            <Slider label="Vy" value={vy[i]} min={-3} max={3} step={0.05} color={BODY_COLORS[i]} onChange={v => handleVy(i, v)} />
                        </div>
                    ))}
                </div>

                {/* Launch buttons */}
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2.5rem', flexWrap: 'wrap' }}>
                    <button onClick={handleLaunch} style={{
                        fontFamily: '"IBM Plex Mono", monospace',
                        fontSize: '0.85rem',
                        letterSpacing: '0.15em',
                        color: '#05070A',
                        background: '#00F0FF',
                        border: 'none',
                        borderRadius: '4px',
                        padding: '0.85rem 2.5rem',
                        cursor: 'pointer',
                        fontWeight: 600,
                        transition: 'opacity 0.2s',
                    }}>
                        ▶ LAUNCH SIMULATION
                    </button>
                    <button onClick={handleRandom} style={{
                        fontFamily: '"IBM Plex Mono", monospace',
                        fontSize: '0.85rem',
                        letterSpacing: '0.15em',
                        color: '#00F0FF',
                        background: 'transparent',
                        border: '1px solid #00F0FF',
                        borderRadius: '4px',
                        padding: '0.85rem 2.5rem',
                        cursor: 'pointer',
                        transition: 'background 0.2s',
                    }}>
                        ⚄ RANDOM CONDITIONS
                    </button>
                </div>

                {/* Footer note */}
                <p style={{ fontFamily: '"IBM Plex Mono", monospace', color: 'rgba(232,228,221,0.25)', fontSize: '0.65rem', textAlign: 'center', marginTop: '2rem', letterSpacing: '0.1em' }}>
                    Tip: try symmetric velocities (e.g. Vx = 0) for near-periodic orbits.
                </p>
            </div>
        </section>
    );
};
