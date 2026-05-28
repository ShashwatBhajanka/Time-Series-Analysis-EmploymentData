import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statsmodels.api as sm
import numpy as np
import warnings
import os

os.makedirs("figures", exist_ok=True)

plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})

df = pd.read_csv("employment.csv", parse_dates = ["date"])
df = df.sort_values("date")
df = df.asfreq("MS")

series = df["overall_rate"]

