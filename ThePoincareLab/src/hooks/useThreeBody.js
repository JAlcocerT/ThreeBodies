import { useRef, useCallback } from 'react';

// Gravitational constant scaled for visual units
const G = 0.5;

const computeAccelerations = (positions, masses) => {
    const acc = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            if (i === j) continue;
            const dx = positions[j][0] - positions[i][0];
            const dy = positions[j][1] - positions[i][1];
            const dz = positions[j][2] - positions[i][2];
            const distSq = dx * dx + dy * dy + dz * dz;
            // Softening avoids singularities when bodies overlap
            const softened = distSq + 0.01;
            const invDist3 = 1.0 / (softened * Math.sqrt(softened));
            const f = G * masses[j] * invDist3;
            acc[i][0] += f * dx;
            acc[i][1] += f * dy;
            acc[i][2] += f * dz;
        }
    }
    return acc;
};

const rk4Step = (positions, velocities, masses, dt) => {
    const k1v = computeAccelerations(positions, masses);
    const k1p = velocities;

    const p2 = positions.map((p, i) => [
        p[0] + 0.5 * dt * k1p[i][0],
        p[1] + 0.5 * dt * k1p[i][1],
        p[2] + 0.5 * dt * k1p[i][2],
    ]);
    const v2 = velocities.map((v, i) => [
        v[0] + 0.5 * dt * k1v[i][0],
        v[1] + 0.5 * dt * k1v[i][1],
        v[2] + 0.5 * dt * k1v[i][2],
    ]);
    const k2v = computeAccelerations(p2, masses);
    const k2p = v2;

    const p3 = positions.map((p, i) => [
        p[0] + 0.5 * dt * k2p[i][0],
        p[1] + 0.5 * dt * k2p[i][1],
        p[2] + 0.5 * dt * k2p[i][2],
    ]);
    const v3 = velocities.map((v, i) => [
        v[0] + 0.5 * dt * k2v[i][0],
        v[1] + 0.5 * dt * k2v[i][1],
        v[2] + 0.5 * dt * k2v[i][2],
    ]);
    const k3v = computeAccelerations(p3, masses);
    const k3p = v3;

    const p4 = positions.map((p, i) => [
        p[0] + dt * k3p[i][0],
        p[1] + dt * k3p[i][1],
        p[2] + dt * k3p[i][2],
    ]);
    const v4 = velocities.map((v, i) => [
        v[0] + dt * k3v[i][0],
        v[1] + dt * k3v[i][1],
        v[2] + dt * k3v[i][2],
    ]);
    const k4v = computeAccelerations(p4, masses);
    const k4p = v4;

    const nextPositions = positions.map((p, i) => [
        p[0] + (dt / 6) * (k1p[i][0] + 2 * k2p[i][0] + 2 * k3p[i][0] + k4p[i][0]),
        p[1] + (dt / 6) * (k1p[i][1] + 2 * k2p[i][1] + 2 * k3p[i][1] + k4p[i][1]),
        p[2] + (dt / 6) * (k1p[i][2] + 2 * k2p[i][2] + 2 * k3p[i][2] + k4p[i][2]),
    ]);
    const nextVelocities = velocities.map((v, i) => [
        v[0] + (dt / 6) * (k1v[i][0] + 2 * k2v[i][0] + 2 * k3v[i][0] + k4v[i][0]),
        v[1] + (dt / 6) * (k1v[i][1] + 2 * k2v[i][1] + 2 * k3v[i][1] + k4v[i][1]),
        v[2] + (dt / 6) * (k1v[i][2] + 2 * k2v[i][2] + 2 * k3v[i][2] + k4v[i][2]),
    ]);

    return { nextPositions, nextVelocities };
};

export const useThreeBody = (initialPositions, initialVelocities, initialMasses) => {
    const posRef = useRef(initialPositions.map(p => [...p]));
    const velRef = useRef(initialVelocities.map(v => [...v]));
    const massRef = useRef([...initialMasses]);
    const trailRef = useRef([[], [], []]);
    const MAX_TRAIL = 200;

    const step = useCallback((dt, dilation, subSteps) => {
        const actualDt = (dt * dilation) / subSteps;
        let pos = posRef.current;
        let vel = velRef.current;
        const masses = massRef.current;

        for (let s = 0; s < subSteps; s++) {
            const { nextPositions, nextVelocities } = rk4Step(pos, vel, masses, actualDt);
            pos = nextPositions;
            vel = nextVelocities;
        }

        posRef.current = pos;
        velRef.current = vel;

        for (let b = 0; b < 3; b++) {
            trailRef.current[b].push([pos[b][0], pos[b][1]]);
            if (trailRef.current[b].length > MAX_TRAIL) {
                trailRef.current[b].shift();
            }
        }
    }, []);

    const setMass = useCallback((index, value) => {
        massRef.current[index] = value;
    }, []);

    const resetTrails = useCallback(() => {
        trailRef.current = [[], [], []];
    }, []);

    return { posRef, velRef, massRef, trailRef, step, setMass, resetTrails };
};
