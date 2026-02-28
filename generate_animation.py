import numpy as np
import cv2
import argparse
import sys
import os

# Cosmic Entropy Palette
PALETTE = {
    'void': (10, 7, 5),          # #05070A in BGR
    'pulsar': (255, 240, 0),     # #00F0FF in BGR
    'horizon': (46, 11, 26),      # #1A0B2E in BGR
    'paper': (221, 228, 232),     # #E8E4DD in BGR
    'supernova': (255, 255, 255), # #FFFFFF in BGR
    'violet': (255, 95, 191)      # Match web app violet Beta Beta
}

# Body colors to match web app
BODY_COLORS = [
    PALETTE['pulsar'],
    PALETTE['violet'],
    PALETTE['supernova']
]

def compute_accelerations(pos, masses, G):
    acc = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            if i == j: continue
            diff = pos[j] - pos[i]
            dist_sq = np.sum(diff**2)
            softened = dist_sq + 0.01
            f = G * masses[j] / (softened * np.sqrt(softened))
            acc[i] += f * diff
    return acc

def rk4_step(pos, vel, masses, G, dt):
    # k1
    a1 = compute_accelerations(pos, masses, G)
    v1 = vel
    
    # k2
    p2 = pos + 0.5 * dt * v1
    v2 = vel + 0.5 * dt * a1
    a2 = compute_accelerations(p2, masses, G)
    
    # k3
    p3 = pos + 0.5 * dt * v2
    v3 = vel + 0.5 * dt * a2
    a3 = compute_accelerations(p3, masses, G)
    
    # k4
    p4 = pos + dt * v3
    v4 = vel + dt * a3
    a4 = compute_accelerations(p4, masses, G)
    
    next_pos = pos + (dt / 6.0) * (v1 + 2*v2 + 2*v3 + v4)
    next_vel = vel + (dt / 6.0) * (a1 + 2*a2 + 2*a3 + a4)
    
    return next_pos, next_vel

def draw_glow(img, center, radius, color, alpha=0.5):
    """Draws a soft glow effect around the body"""
    # Create an overlay for the glow
    overlay = img.copy()
    # Draw several concentric circles with decreasing opacity
    for r in range(radius * 5, radius, -2):
        strength = max(0, alpha * (1.0 - (r - radius) / (radius * 4)))
        cv2.circle(overlay, center, r, color, -1, lineType=cv2.LINE_AA)
        cv2.addWeighted(overlay, strength * 0.1, img, 1.0 - strength * 0.1, 0, img)

def main():
    parser = argparse.ArgumentParser(description='Generate Three-Body Simulation Video')
    parser.add_argument('--masses', type=float, nargs=3, default=[1.0, 1.0, 1.0], help='Masses of the three bodies')
    parser.add_argument('--pos', type=float, nargs=6, default=[-2.0, 0.5, 2.0, -0.5, 0.0, 2.0], help='Initial XY positions (x1 y1 x2 y2 x3 y3)')
    parser.add_argument('--vel', type=float, nargs=6, default=[0.0, 0.6, 0.0, -0.6, -0.6, 0.0], help='Initial velocities (vx1 vy1 vx2 vy2 vx3 vy3)')
    parser.add_argument('--duration', type=float, default=10.0, help='Duration of video in seconds')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    parser.add_argument('--res', type=int, nargs=2, default=[1920, 1080], help='Resolution (width height)')
    parser.add_argument('--output', type=str, default='simulation.mp4', help='Output filename')
    parser.add_argument('--trail_len', type=int, default=150, help='Length of the trails in frames')
    parser.add_argument('--scale', type=float, default=150.0, help='Visual scale (pixels per unit)')
    parser.add_argument('--substeps', type=int, default=10, help='Physics sub-steps per frame')

    args = parser.parse_args()

    W, H = args.res
    G = 0.5 # Match web app visual G
    
    # Initialize state
    masses = np.array(args.masses)
    pos = np.array([
        [args.pos[0], args.pos[1], 0.0],
        [args.pos[2], args.pos[3], 0.0],
        [args.pos[4], args.pos[5], 0.0]
    ])
    vel = np.array([
        [args.vel[0], args.vel[1], 0.0],
        [args.vel[2], args.vel[3], 0.0],
        [args.vel[4], args.vel[5], 0.0]
    ])

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(args.output, fourcc, args.fps, (W, H))

    num_frames = int(args.duration * args.fps)
    dt = 1.0 / args.fps
    
    history = [[] for _ in range(3)]
    
    print(f"Generating {num_frames} frames to {args.output}...")

    for f in range(num_frames):
        # Physics Step
        for _ in range(args.substeps):
            pos, vel = rk4_step(pos, vel, masses, G, dt / args.substeps)
        
        # Add to history
        for i in range(3):
            history[i].append(pos[i][:2].copy())
            if len(history[i]) > args.trail_len:
                history[i].pop(0)

        # Rendering
        # Start with Void background
        frame = np.full((H, W, 3), PALETTE['void'], dtype=np.uint8)
        
        # Optional: Add radial gradient background (approximated)
        # Center of mass for camera following
        total_m = np.sum(masses)
        com = np.sum(pos.T * masses, axis=1) / total_m
        
        cx, cy = W // 2, H // 2
        offset_x = cx - com[0] * args.scale
        offset_y = cy - com[1] * args.scale

        # Draw Trails
        for i in range(3):
            if len(history[i]) < 2: continue
            points = np.array([(offset_x + p[0] * args.scale, offset_y + p[1] * args.scale) for p in history[i]], dtype=np.int32)
            cv2.polylines(frame, [points], False, BODY_COLORS[i], thickness=2, lineType=cv2.LINE_AA)

        # Draw Bodies with bloom
        for i in range(3):
            px = int(offset_x + pos[i][0] * args.scale)
            py = int(offset_y + pos[i][1] * args.scale)
            
            # Glow/Bloom
            draw_glow(frame, (px, py), 10, BODY_COLORS[i], alpha=0.4)
            
            # Core
            cv2.circle(frame, (px, py), 6, BODY_COLORS[i], -1, lineType=cv2.LINE_AA)
            cv2.circle(frame, (px, py), 8, (255, 255, 255), 1, lineType=cv2.LINE_AA) # Edge highlight

        # Add some telemetry (Simulated)
        text_color = PALETTE['pulsar']
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "THE POINCARE LAB RENDERER", (50, 50), font, 1.0, text_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"FRAME: {f:04d} / {num_frames}", (50, 90), font, 0.7, text_color, 1, cv2.LINE_AA)
        cv2.putText(frame, f"COM: [{com[0]:.2f}, {com[1]:.2f}]", (50, 120), font, 0.7, text_color, 1, cv2.LINE_AA)

        out.write(frame)
        
        if f % 30 == 0:
            sys.stdout.write(f"\rProgress: {100.0 * f / num_frames:.1f}%")
            sys.stdout.flush()

    print("\nEncoding complete.")
    out.release()

if __name__ == "__main__":
    main()
