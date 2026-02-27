import React from 'react';

export const HeroOverlay = ({ posRef }) => {
    return (
        <div style={{
            position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
            background: 'radial-gradient(ellipse at 50% 110%, rgba(26,11,46,0.9) 0%, rgba(5,7,10,0.3) 60%)',
            zIndex: 10,
            pointerEvents: 'none',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            padding: '2.5rem',
            boxSizing: 'border-box',
        }}>

            {/* Top-right: Telemetry */}
            <div style={{ alignSelf: 'flex-end', textAlign: 'right', fontFamily: '"IBM Plex Mono", monospace', fontSize: '0.72rem', letterSpacing: '0.12em', userSelect: 'none' }}>
                <div style={{ color: '#00F0FF', marginBottom: '0.25rem' }}>SYSTEM // CHAOTIC TRIPLE-SUN</div>
                <div style={{ color: 'rgba(232,228,221,0.7)' }}>INTEGRATOR: RK4 ▸ ACTIVE</div>
                <div style={{ color: 'rgba(232,228,221,0.5)', marginTop: '0.5rem' }}>Δt = 0.016 ms</div>
            </div>

            {/* Bottom-left: Brand */}
            <div style={{ maxWidth: '36rem' }}>
                <div style={{ color: '#00F0FF', fontFamily: '"IBM Plex Mono", monospace', fontSize: '0.72rem', letterSpacing: '0.3em', marginBottom: '1rem', textTransform: 'uppercase' }}>
                    Observatory 04 — The Poincaré Lab
                </div>
                <h1 style={{
                    fontFamily: '"IBM Plex Sans", sans-serif',
                    fontSize: 'clamp(3rem, 10vw, 7rem)',
                    fontWeight: 700,
                    lineHeight: 1,
                    color: '#FFFFFF',
                    margin: 0,
                    textShadow: '0 0 40px rgba(0,240,255,0.4)',
                    letterSpacing: '-0.02em',
                }}>
                    THE<br />POINCARÉ<br />LAB
                </h1>
                <p style={{
                    fontFamily: '"IBM Plex Sans", sans-serif',
                    color: 'rgba(232,228,221,0.75)',
                    fontSize: '1.05rem',
                    maxWidth: '28rem',
                    lineHeight: 1.65,
                    marginTop: '1.25rem',
                }}>
                    A real-time numeric study of{' '}
                    <span style={{ color: '#00F0FF' }}>gravitational chaos</span>{' '}
                    and the brutal sensitivity of initial conditions.
                </p>
                <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
                    <a href="#laboratory" style={{
                        fontFamily: '"IBM Plex Mono", monospace', fontSize: '0.8rem',
                        color: '#00F0FF', border: '1px solid #00F0FF',
                        padding: '0.6rem 1.4rem', borderRadius: '2px',
                        textDecoration: 'none', letterSpacing: '0.15em',
                        transition: 'background 0.2s',
                        pointerEvents: 'all',
                    }}>
                        ENTER LAB ↓
                    </a>
                </div>
            </div>
        </div>
    );
};
