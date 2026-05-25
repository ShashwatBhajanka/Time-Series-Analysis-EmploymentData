import numpy as np
import pandas as pd
import matplotlib
import data_profiling
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sb
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from data_profiling import ProfileReport
import statsmodels.api as sm

df = pd.read_csv("employment.csv")
df['date'] = pd.to_datetime(df['date'])


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

def hiringageovertime():   
    df['year'] = df['date'].dt.year
    df_year = df.drop(columns=['date']).groupby('year').mean(numeric_only=True)

    df_year.plot(figsize=(15, 8))
    plt.title('Unemployment Rate over the Years')
    plt.xlabel('Year')
    plt.ylabel('Unemployment Rate (%)')
    plt.legend(loc='upper right', fontsize=8)
    plt.show()

