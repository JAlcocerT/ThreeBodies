import { useRef, useEffect } from 'react';

// Body colors: Pulsar Cyan, Violet, Supernova White
const COLORS = ['#00F0FF', '#BF5FFF', '#FFFFFF'];
const SCALE = 100; // pixels per visual unit

export const SimulationCanvas = ({ engine, timeDilation }) => {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let animId;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        const draw = () => {
            engine.step(0.016, timeDilation, 8);

            const W = canvas.width;
            const H = canvas.height;

            // Soft fade for motion blur
            ctx.fillStyle = 'rgba(5, 7, 10, 0.25)';
            ctx.fillRect(0, 0, W, H);

            const pos = engine.posRef.current;
            const masses = engine.massRef.current;

            // Camera follows center of mass
            const totalM = masses[0] + masses[1] + masses[2];
            let comX = 0, comY = 0;
            for (let i = 0; i < 3; i++) {
                comX += pos[i][0] * masses[i];
                comY += pos[i][1] * masses[i];
            }
            comX /= totalM;
            comY /= totalM;

            const cx = W / 2 - comX * SCALE;
            const cy = H / 2 - comY * SCALE;

            // Draw trails
            const trails = engine.trailRef.current;
            for (let i = 0; i < 3; i++) {
                const trail = trails[i];
                if (trail.length < 2) continue;

                ctx.beginPath();
                ctx.moveTo(cx + trail[0][0] * SCALE, cy + trail[0][1] * SCALE);
                for (let t = 1; t < trail.length; t++) {
                    ctx.lineTo(cx + trail[t][0] * SCALE, cy + trail[t][1] * SCALE);
                }
                ctx.strokeStyle = COLORS[i];
                ctx.lineWidth = 1.5;
                ctx.globalAlpha = 0.35;
                ctx.stroke();
                ctx.globalAlpha = 1.0;
            }

            // Draw bodies with bloom
            for (let i = 0; i < 3; i++) {
                const x = cx + pos[i][0] * SCALE;
                const y = cy + pos[i][1] * SCALE;

                // Outer glow
                const grad = ctx.createRadialGradient(x, y, 0, x, y, 40);
                grad.addColorStop(0, COLORS[i] + 'CC');
                grad.addColorStop(1, COLORS[i] + '00');
                ctx.beginPath();
                ctx.arc(x, y, 40, 0, Math.PI * 2);
                ctx.fillStyle = grad;
                ctx.fill();

                // Core
                ctx.beginPath();
                ctx.arc(x, y, 8, 0, Math.PI * 2);
                ctx.shadowBlur = 30;
                ctx.shadowColor = COLORS[i];
                ctx.fillStyle = COLORS[i];
                ctx.fill();
                ctx.shadowBlur = 0;
            }

            animId = requestAnimationFrame(draw);
        };

        draw();
        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animId);
        };
    }, [engine, timeDilation]);

    return (
        <canvas
            ref={canvasRef}
            style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', zIndex: 0 }}
        />
    );
};
