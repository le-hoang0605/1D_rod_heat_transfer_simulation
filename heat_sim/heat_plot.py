# heat_plot.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.collections import LineCollection
from matplotlib import cm
from heat_core import setup_matrices, compute_next_u

def run_plot(L, alpha, f, back_callback):
    nx = 101
    dx = L / (nx - 1)
    x = np.linspace(0, L, nx)
    u = f(x)
    sigma = 0.5
    dt = sigma * dx**2 / alpha
    r = alpha * dt / dx**2
    M_imp, M_exp = setup_matrices(nx, r)

    # Plot
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, L)
    global_min = np.min(u)
    global_max = np.max(u)
    ax.set_ylim(global_min - 1, global_max + 1)
    ax.set_xlabel('Position (x)')
    ax.set_ylabel('Temperature (u(x,t))')
    ax.set_title('Heat Distribution Over Time')

    # Gradient-colored line
    norm = plt.Normalize(global_min, global_max)
    cmap = cm.jet  # Blue (low) to red (high)
    points = np.array([x, u]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, norm=norm, linewidth=3)
    lc.set_array(u)
    ax.add_collection(lc)

    # Back Button
    btn_ax = plt.axes([0.84, 0.02, 0.13, 0.05], facecolor='#37474F')
    back_btn = Button(btn_ax, 'Back to Input', color='#37474F', hovercolor='#455A64')
    for spine in btn_ax.spines.values():
        spine.set_color('#78909C')
        spine.set_linewidth(1.5)
        spine.set_capstyle('round')
    back_btn.label.set_color('white')
    back_btn.label.set_fontsize(9)
    back_btn.label.set_fontweight('bold')

    def on_back_click(event):
        plt.close(fig)
        back_callback()

    back_btn.on_clicked(on_back_click)

    # Animation
    steps_per_frame = 10
    num_frames = 200

    def update(frame):
        nonlocal u
        for _ in range(steps_per_frame):
            u = compute_next_u(u, M_imp, M_exp)
        points = np.array([x, u]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc.set_segments(segments)
        lc.set_array(u)
        return lc,

    ani = FuncAnimation(fig, update, frames=num_frames, interval=50, blit=True)
    plt.tight_layout()
    plt.show()