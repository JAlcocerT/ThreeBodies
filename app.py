from flask import Flask, render_template, request
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from threebody import simulate_three_body

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_G = 6.67430e-11
    default_masses = [5e24, 5e24, 5e24]
    default_positions = [[1e11, 0, 0], [-1e11, 0, 0], [0, 1e11, 0]]
    default_velocities = [[0, 2e4, 0], [0, -2e4, 0], [-2e4, 0, 0]]
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
            t, bodies = simulate_three_body([m1, m2, m3], [pos1, pos2, pos3], [vel1, vel2, vel3], G=G)
            traces = []
            colors = ['blue', 'red', 'green']
            for i, body in enumerate(bodies):
                traces.append(go.Scatter3d(
                    x=body[:,0], y=body[:,1], z=body[:,2],
                    mode='lines',
                    name=f'Body {i+1}',
                    line=dict(color=colors[i], width=4)
                ))
            layout = go.Layout(
                title='3-Body Problem Trajectories',
                scene=dict(
                    xaxis_title='X (m)',
                    yaxis_title='Y (m)',
                    zaxis_title='Z (m)'
                ),
                margin=dict(l=0, r=0, b=0, t=40)
            )
            fig = go.Figure(data=traces, layout=layout)
            plot_div = pio.to_html(fig, full_html=False)
        except Exception as e:
            plot_div = f'<div style="color:red">Error: {e}</div>'
    return render_template('index.html',
        default_G=default_G,
        default_masses=default_masses,
        default_positions=default_positions,
        default_velocities=default_velocities,
        plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
