import React, { useState } from 'react';

const BODY_COLORS = ['#00F0FF', '#BF5FFF', '#FFFFFF'];
const BODY_NAMES = ['Pulsar Alpha', 'Violet Beta', 'Nova Gamma'];

const cardStyle = {
    background: 'rgba(5,7,10,0.85)',
    border: '1px solid rgba(0,240,255,0.2)',
    borderRadius: '8px',
    padding: '1.25rem',
    backdropFilter: 'blur(12px)',
    minWidth: '260px',
};

const titleStyle = {
    fontFamily: '"IBM Plex Mono", monospace',
    color: '#00F0FF',
    fontSize: '0.65rem',
    letterSpacing: '0.2em',
    marginBottom: '1rem',
    textTransform: 'uppercase',
};

export const Laboratory = ({ engine, onTimeDilation }) => {
    const initialMasses = engine.massRef.current;
    const [masses, setMasses] = useState([...initialMasses]);
    const [dilation, setDilation] = useState(1.0);

    const handleMass = (i, val) => {
        const v = parseFloat(val);
        const next = [...masses];
        next[i] = v;
        setMasses(next);
        engine.setMass(i, v);
    };

    const handleDilation = (val) => {
        const v = parseFloat(val);
        setDilation(v);
        onTimeDilation(v);
    };

    return (
        <div id="laboratory" style={{
            position: 'absolute', bottom: '2rem', right: '2rem',
            display: 'flex', flexDirection: 'column', gap: '0.75rem',
            zIndex: 20, pointerEvents: 'all',
        }}>
            {/* Mass Constructor */}
            <div style={cardStyle}>
                <div style={titleStyle}>// Mass Constructor</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {masses.map((m, i) => (
                        <div key={i}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: '"IBM Plex Mono", monospace', fontSize: '0.7rem', marginBottom: '0.3rem' }}>
                                <span style={{ color: BODY_COLORS[i] }}>{BODY_NAMES[i]}</span>
                                <span style={{ color: 'rgba(232,228,221,0.5)' }}>{m.toFixed(2)} M</span>
                            </div>
                            <input
                                type="range" min="0.2" max="5.0" step="0.05" value={m}
                                onChange={e => handleMass(i, e.target.value)}
                                style={{ width: '100%', accentColor: BODY_COLORS[i], cursor: 'pointer' }}
                            />
                        </div>
                    ))}
                </div>
            </div>

            {/* Temporal Governor */}
            <div style={cardStyle}>
                <div style={titleStyle}>// Temporal Governor</div>
                <div style={{ fontFamily: '"IBM Plex Mono", monospace', fontSize: '0.7rem', color: '#00F0FF', marginBottom: '0.5rem' }}>
                    Time Dilation: {dilation.toFixed(1)}×
                </div>
                <input
                    type="range" min="0.1" max="5.0" step="0.1" value={dilation}
                    onChange={e => handleDilation(e.target.value)}
                    style={{ width: '100%', accentColor: '#00F0FF', cursor: 'pointer' }}
                />
                <button
                    onClick={() => engine.resetTrails()}
                    style={{
                        marginTop: '0.75rem', width: '100%',
                        fontFamily: '"IBM Plex Mono", monospace', fontSize: '0.7rem',
                        color: '#00F0FF', background: 'transparent',
                        border: '1px solid rgba(0,240,255,0.3)', borderRadius: '4px',
                        padding: '0.4rem', cursor: 'pointer', letterSpacing: '0.1em',
                        transition: 'border-color 0.2s',
                    }}
                >
                    RESET TRACES
                </button>
            </div>
        </div>
    );
};
