import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sb
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
    lc = df.plot(subplots = True, figsize = (10,20))
    plt.xlabel("Year")
    plt.ylabel("Unemployment Rate")
    plt.show()
    
lineplot()
    