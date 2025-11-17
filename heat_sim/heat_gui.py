# heat_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from heat_core import metals, parse_initial_condition
from heat_plot import run_plot

gui_root = None
gui_widgets = {}

def start_simulation():
    try:
        L = float(gui_widgets['length'].get())
        if L <= 0:
            raise ValueError("Length must be positive.")
        metal = gui_widgets['metal'].get().lower()
        alpha = metals.get(metal)
        if alpha is None:
            raise ValueError("Please select a metal.")
        init_expr = gui_widgets['expr'].get()
        f = parse_initial_condition(init_expr, L)
        gui_root.withdraw()
        run_plot(L, alpha, f, back_callback=gui_root.deiconify)
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error",
            f"Invalid expression: {e}\n\nExample: sin(pi * x / L)")

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [x1 + radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True, splinesteps=20)

def create_gui():
    global gui_root, gui_widgets
    gui_root = tk.Tk()
    gui_root.title("Heat Transfer Simulator")
    gui_root.geometry("600x500")
    gui_root.configure(bg='#212121')
    gui_root.resizable(False, False)

    # === Style ===
    style = ttk.Style()
    style.theme_use('clam')
    # Configure dark theme
    style.configure('TLabel', background='#212121', foreground='#FFFFFF', font=('Helvetica', 11))
    style.configure('TButton', font=('Helvetica', 11, 'bold'))
    style.configure('TCombobox', fieldbackground='#424242', background='#424242', foreground='#FFFFFF')
    style.map('TCombobox', fieldbackground=[('readonly', '#424242')])
    style.map('TCombobox', selectbackground=[('readonly', '#4FC3F7')])

    # === Title ===
    title = tk.Label(gui_root, text="Heat Transfer Simulator", bg='#212121', fg='#4FC3F7',
                     font=('Helvetica', 16, 'bold'))
    title.pack(pady=(25, 15))

    # === Rod Length ===
    tk.Label(gui_root, text="Rod Length (meters):").pack(pady=(15, 5))
    entry_length = tk.Entry(gui_root, width=20, font=('Consolas', 11), bg='#424242', fg='#FFFFFF',
                            insertbackground='#FFFFFF', relief='flat', bd=5)
    entry_length.pack(pady=5)
    entry_length.insert(0, "1.0")
    gui_widgets['length'] = entry_length

    # === Metal Type ===
    tk.Label(gui_root, text="Metal Type:").pack(pady=(15, 5))
    combo_metal = ttk.Combobox(gui_root, values=list(metals.keys()), state="readonly", width=18)
    combo_metal.pack(pady=5)
    combo_metal.set("iron")
    gui_widgets['metal'] = combo_metal

    # === Initial Temp ===
    tk.Label(gui_root, text="Initial Temperature f(x):").pack(pady=(15, 5))
    entry_expr = tk.Entry(gui_root, width=40, font=('Consolas', 11), bg='#424242', fg='#FFFFFF',
                          insertbackground='#FFFFFF', relief='flat', bd=5)
    entry_expr.pack(pady=5)
    entry_expr.insert(0, "sin(pi * x / 0.5)")
    gui_widgets['expr'] = entry_expr

    # === Start Button (Rounded Rectangle) ===
    start_btn = tk.Canvas(gui_root, width=200, height=50, bg='#212121', highlightthickness=0)
    start_btn.pack(pady=25)
    # Draw rounded rectangle
    btn_rect = create_rounded_rectangle(start_btn, 10, 5, 190, 45, radius=20, fill='#4FC3F7')
    # Button text
    btn_text = start_btn.create_text(100, 25, text="Start Simulation", fill='white',
                                     font=('Helvetica', 12, 'bold'))

    def on_enter(e):
        start_btn.itemconfig(btn_rect, fill='#29B6F6')

    def on_leave(e):
        start_btn.itemconfig(btn_rect, fill='#4FC3F7')

    def on_click(e):
        start_simulation()

    start_btn.tag_bind(btn_rect, '<Enter>', on_enter)
    start_btn.tag_bind(btn_rect, '<Leave>', on_leave)
    start_btn.tag_bind(btn_rect, '<Button-1>', on_click)
    start_btn.tag_bind(btn_text, '<Enter>', on_enter)
    start_btn.tag_bind(btn_text, '<Leave>', on_leave)
    start_btn.tag_bind(btn_text, '<Button-1>', on_click)

    # === Close ===
    gui_root.protocol("WM_DELETE_WINDOW", gui_root.quit)
    gui_root.mainloop()