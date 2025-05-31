from flask import Flask, render_template, request
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from threebody import simulate_three_body

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_G = 6.67430e-11
    default_masses = [70, 80, 60]  # kg, human scale
    default_positions = [[0, 0, 0], [2, 0, 0], [1, 1.5, 0]]  # meters
    default_velocities = [[0, 0, 0], [0, 0.2, 0], [0.2, 0, 0]]  # m/s
    default_tmax = 60  # seconds
    default_steps = 200
    plot_div = None
    if request.method == 'POST':
        try:
            m1 = float(request.form['m1'])
            m2 = float(request.form['m2'])
            m3 = float(request.form['m3'])
            pos1 = [float(request.form['x1']), float(request.form['y1']), float(request.form['z1'])]
            pos2 = [float(request.form['x2']), float(request.form['y2']), float(request.form['z2'])]
            pos3 = [float(request.form['x3']), float(request.form['y3']), float(request.form['z3'])]
            vel1 = [float(request.form['vx1']), float(request.form['vy1']), float(request.form['vz1'])]
            vel2 = [float(request.form['vx2']), float(request.form['vy2']), float(request.form['vz2'])]
            vel3 = [float(request.form['vx3']), float(request.form['vy3']), float(request.form['vz3'])]
            G = float(request.form['G'])
            tmax = float(request.form['tmax'])
            steps = int(request.form['steps'])
            t, bodies = simulate_three_body([m1, m2, m3], [pos1, pos2, pos3], [vel1, vel2, vel3], G=G, t_span=(0, tmax), t_eval=np.linspace(0, tmax, steps))
            colors = ['blue', 'red', 'green']
            # Animation frames for slider
            frames = []
            for k in range(len(t)):
                data = [go.Scatter3d(x=[bodies[i][k,0]], y=[bodies[i][k,1]], z=[bodies[i][k,2]],
                                     mode='markers', marker=dict(size=8, color=colors[i]), name=f'Body {i+1}') for i in range(3)]
                frames.append(go.Frame(data=data, name=str(k)))
            # Full trajectory lines
            traces = [go.Scatter3d(x=bodies[i][:,0], y=bodies[i][:,1], z=bodies[i][:,2],
                                   mode='lines', line=dict(color=colors[i], width=2), name=f'Body {i+1} Path') for i in range(3)]
            # Initial positions for animation
            data = [go.Scatter3d(x=[bodies[i][0,0]], y=[bodies[i][0,1]], z=[bodies[i][0,2]],
                                 mode='markers', marker=dict(size=8, color=colors[i]), name=f'Body {i+1}') for i in range(3)]
            layout = go.Layout(
                title='3-Body Problem (Human Scale)',
                scene=dict(xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Z (m)'),
                margin=dict(l=0, r=0, b=0, t=40),
                updatemenus=[dict(type='buttons', showactive=False, y=1, x=1.2,
                                 buttons=[dict(label='Play', method='animate', args=[[None], {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True}]),
                                          dict(label='Pause', method='animate', args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}])])],
                sliders=[dict(
                    steps=[dict(method='animate', args=[[str(k)], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}], label=f'{t[k]:.2f}s') for k in range(len(t))],
                    transition={'duration': 0}, x=0.1, y=0, currentvalue={'prefix': 'Time: '}, len=0.9
                )]
            )
            fig = go.Figure(data=traces+data, layout=layout, frames=frames)
            plot_div = pio.to_html(fig, full_html=False)
        except Exception as e:
            plot_div = f'<div style="color:red">Error: {e}</div>'
    return render_template('index.html',
        default_G=default_G,
        default_masses=default_masses,
        default_positions=default_positions,
        default_velocities=default_velocities,
        default_tmax=default_tmax,
        default_steps=default_steps,
        plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
