from flask import Flask, render_template, request, session
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from threebody import simulate_three_body

app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_random_key'  # Needed for session

@app.route('/', methods=['GET', 'POST'])
def index():
    default_G = 6.67430e-11
    default_masses = [7000000, 8000000, 6000000]  # kg, human scale
    default_positions = [[0, 0, 0], [2, 0, 0], [1, 1.5, 0]]  # meters
    default_velocities = [[0, 0, 0], [0, 0.2, 0], [0.2, 0, 0]]  # m/s
    default_tmax = 60  # seconds
    default_steps = 200

    # Try to get last-used values from session
    session_defaults = session.get('params', {})
    def get_param(name, fallback):
        return session_defaults.get(name, fallback)

    default_G = get_param('G', default_G)
    default_masses = [get_param(f'm{i+1}', default_masses[i]) for i in range(3)]
    default_positions = [[get_param(f'x{i+1}', default_positions[i][0]),
                          get_param(f'y{i+1}', default_positions[i][1]),
                          get_param(f'z{i+1}', default_positions[i][2])] for i in range(3)]
    default_velocities = [[get_param(f'vx{i+1}', default_velocities[i][0]),
                           get_param(f'vy{i+1}', default_velocities[i][1]),
                           get_param(f'vz{i+1}', default_velocities[i][2])] for i in range(3)]
    default_tmax = get_param('tmax', default_tmax)
    default_steps = get_param('steps', default_steps)

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
            # Save current params to session
            session['params'] = {
                'm1': m1, 'm2': m2, 'm3': m3,
                'x1': pos1[0], 'y1': pos1[1], 'z1': pos1[2],
                'x2': pos2[0], 'y2': pos2[1], 'z2': pos2[2],
                'x3': pos3[0], 'y3': pos3[1], 'z3': pos3[2],
                'vx1': vel1[0], 'vy1': vel1[1], 'vz1': vel1[2],
                'vx2': vel2[0], 'vy2': vel2[1], 'vz2': vel2[2],
                'vx3': vel3[0], 'vy3': vel3[1], 'vz3': vel3[2],
                'G': G, 'tmax': tmax, 'steps': steps
            }
            t, bodies = simulate_three_body([m1, m2, m3], [pos1, pos2, pos3], [vel1, vel2, vel3], G=G, t_span=(0, tmax), t_eval=np.linspace(0, tmax, steps))
            colors = ['blue', 'red', 'green']
            # Animation frames for slider
            frames = []
            for k in range(len(t)):
                # For each frame, show the trace up to time k and the current marker
                frame_data = []
                for i in range(3):
                    frame_data.append(go.Scatter3d(
                        x=bodies[i][:k+1,0], y=bodies[i][:k+1,1], z=bodies[i][:k+1,2],
                        mode='lines', line=dict(color=colors[i], width=3), name=f'Body {i+1} Path ({colors[i]})',
                        showlegend=False
                    ))
                    frame_data.append(go.Scatter3d(
                        x=[bodies[i][k,0]], y=[bodies[i][k,1]], z=[bodies[i][k,2]],
                        mode='markers', marker=dict(size=8, color=colors[i]), name=f'Body {i+1} ({colors[i]})',
                        showlegend=False
                    ))
                frames.append(go.Frame(data=frame_data, name=str(k)))
            # For the initial frame, show only the starting points and empty traces, with legend
            initial_data = []
            for i in range(3):
                initial_data.append(go.Scatter3d(
                    x=[bodies[i][0,0]], y=[bodies[i][0,1]], z=[bodies[i][0,2]],
                    mode='markers', marker=dict(size=8, color=colors[i]), name=f'Body {i+1} ({colors[i]})', showlegend=True
                ))
                initial_data.append(go.Scatter3d(
                    x=[], y=[], z=[], mode='lines', line=dict(color=colors[i], width=3), name=f'Body {i+1} Path ({colors[i]})', showlegend=True
                ))
            layout = go.Layout(
                title='3-Body Problem (Human Scale)',
                scene=dict(xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Z (m)'),
                margin=dict(l=0, r=0, b=0, t=40),
                showlegend=True,
                legend=dict(x=1.02, y=1, bgcolor='rgba(255,255,255,0.8)', bordercolor='black'),
                updatemenus=[dict(type='buttons', showactive=False, y=1, x=1.2,
                                 buttons=[dict(label='Play', method='animate', args=[[None], {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True}]),
                                          dict(label='Pause', method='animate', args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}])])],
                sliders=[dict(
                    steps=[dict(method='animate', args=[[str(k)], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}], label=f'{t[k]:.2f}s') for k in range(len(t))],
                    transition={'duration': 0}, x=0.1, y=0, currentvalue={'prefix': 'Time: '}, len=0.9
                )]
            )
            fig = go.Figure(data=initial_data, layout=layout, frames=frames)


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
