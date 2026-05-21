import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sb
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# pyrefly: ignore [missing-import]
from ydata_profiling import ProfileReport

df = pd.read_csv("employment.csv")

def AgeWiseBox():
    plt.figure(figsize = (15,8))
    ax = sb.boxplot(data = df)
    ax.set_title("Age wise unemployment")
    plt.xticks(rotation  = 90)
    ax.set_xlabel('Industry')
    ax.set_ylabel('Unemployment Rate')
    plt.show()

def lineplot():
    df['date'] = pd.to_datetime(df['date'])
    age_cols = [c for c in df.columns if c != 'date']
    n = len(age_cols)
    fig, axes = plt.subplots(n, 1, figsize=(12, 3*n), sharex=True)
    for ax, col in zip(axes, age_cols):
        ax.plot(df['date'], df[col])
        ax.set_ylabel(col, fontsize=8)
        ax.tick_params(axis='y', labelsize=7)
    axes[-1].set_xlabel('Year')
    fig.suptitle('Unemployment Rates by Age Group', fontsize=14)
    plt.tight_layout()

    root = tk.Tk()
    root.title('Unemployment Rates by Age Group')
    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    plot_canvas = FigureCanvasTkAgg(fig, scrollable_frame)
    plot_canvas.draw()
    plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(plot_canvas, scrollable_frame)
    toolbar.update()
    root.mainloop()
    
AgeWiseBox()