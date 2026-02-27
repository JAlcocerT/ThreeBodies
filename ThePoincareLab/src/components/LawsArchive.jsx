import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const PANELS = [
    {
        id: '01',
        title: 'The Law of Gravitation',
        law: 'F = G · m₁m₂ / r²',
        body: `In 1687, Newton's Principia established that every particle attracts every other particle with a force proportional to the product of their masses and inversely proportional to the square of their separation. For two bodies, this produces perfect ellipses. For three, it creates an analytical impossibility.`,
    },
    {
        id: '02',
        title: 'The Butterfly Effect',
        law: 'δ(t) ≈ δ₀ · eˡᵗ',
        body: `The three-body problem is chaotic in the deepest mathematical sense. An arbitrarily small perturbation — even on the quantum scale — will diverge exponentially over time. The Lyapunov exponent λ quantifies this divergence. Deterministic yet fundamentally unpredictable.`,
    },
    {
        id: '03',
        title: 'Periodic Solutions',
        law: '∮ ṙ · dr = 0',
        body: `Despite infinite chaos, islands of order exist. In 1993, Chenciner & Montgomery proved the existence of the "Figure-8" orbit — three equal masses chasing each other along a single planar loop forever. Thousands of such choreographies have since been discovered numerically.`,
    },
];

export const LawsArchive = () => {
    const sectionRef = useRef(null);

    useEffect(() => {
        const ctx = gsap.context(() => {
            const panels = gsap.utils.toArray('.law-panel');
            panels.forEach((panel) => {
                ScrollTrigger.create({
                    trigger: panel,
                    start: 'top top',
                    pin: true,
                    pinSpacing: false,
                });
            });
        }, sectionRef);
        return () => ctx.revert();
    }, []);

    return (
        <section ref={sectionRef}>
            {PANELS.map((p, idx) => (
                <div
                    key={p.id}
                    className="law-panel"
                    style={{
                        height: '100vh',
                        width: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        position: 'relative',
                        zIndex: idx + 1,
                        background: idx % 2 === 0
                            ? 'rgba(5,7,10,0.92)'
                            : 'rgba(26,11,46,0.92)',
                        borderTop: '1px solid rgba(0,240,255,0.1)',
                    }}
                >
                    <div style={{
                        maxWidth: '720px',
                        padding: '3rem',
                        border: '1px solid rgba(0,240,255,0.18)',
                        borderRadius: '12px',
                        background: 'rgba(5,7,10,0.6)',
                        backdropFilter: 'blur(16px)',
                        position: 'relative',
                    }}>
                        {/* Corner accents */}
                        <div style={{ position: 'absolute', top: 12, left: 12, width: 24, height: 24, borderTop: '1px solid #00F0FF', borderLeft: '1px solid #00F0FF', opacity: 0.5 }} />
                        <div style={{ position: 'absolute', bottom: 12, right: 12, width: 24, height: 24, borderBottom: '1px solid #00F0FF', borderRight: '1px solid #00F0FF', opacity: 0.5 }} />

                        <div style={{ fontFamily: '"IBM Plex Mono", monospace', color: '#00F0FF', fontSize: '0.65rem', letterSpacing: '0.25em', marginBottom: '0.75rem' }}>
                            ARCHIVE // {p.id}
                        </div>
                        <h2 style={{
                            fontFamily: '"IBM Plex Sans", sans-serif',
                            fontSize: 'clamp(1.8rem, 4vw, 3rem)',
                            fontWeight: 700,
                            color: '#FFFFFF',
                            margin: '0 0 1rem 0',
                            textShadow: '0 0 20px rgba(0,240,255,0.3)',
                        }}>
                            {p.title}
                        </h2>
                        <div style={{
                            fontFamily: '"IBM Plex Mono", monospace',
                            fontSize: '1.2rem',
                            color: '#00F0FF',
                            marginBottom: '1.5rem',
                            padding: '0.75rem 1.25rem',
                            background: 'rgba(0,240,255,0.05)',
                            border: '1px solid rgba(0,240,255,0.15)',
                            borderRadius: '6px',
                            letterSpacing: '0.05em',
                        }}>
                            {p.law}
                        </div>
                        <p style={{
                            fontFamily: '"IBM Plex Sans", sans-serif',
                            color: 'rgba(232,228,221,0.8)',
                            fontSize: '1.05rem',
                            lineHeight: 1.75,
                            margin: 0,
                        }}>
                            {p.body}
                        </p>
                    </div>
                </div>
            ))}
        </section>
    );
};
