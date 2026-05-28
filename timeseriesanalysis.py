import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import statsmodels.api as sm
import warnings
import os

os.makedirs("figures", exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("employment.csv", parse_dates=["date"])
df = df.sort_values("date").set_index("date")

# Core age groups used throughout
age_groups = {
    "age_16_19_rate": "16–19",
    "age_20_24_rate": "20–24",
    "age_25_34_rate": "25–34",
    "age_35_44_rate": "35–44",
    "age_45_54_rate": "45–54",
    "age_55plus_rate": "55+",
}

# NBER recession periods (start, end)
recessions = [
    ("1948-11", "1949-10"), ("1953-07", "1954-05"), ("1957-08", "1958-04"),
    ("1960-04", "1961-02"), ("1969-12", "1970-11"), ("1973-11", "1975-03"),
    ("1980-01", "1980-07"), ("1981-07", "1982-11"), ("1990-07", "1991-03"),
    ("2001-03", "2001-11"), ("2007-12", "2009-06"), ("2020-02", "2020-04"),
]

def shade_recessions(ax):
    """Draw light blue recession bands on a chart."""
    for start, end in recessions:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   color="#d9e8f5", alpha=0.8, zorder=0)

plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.3, "grid.linestyle": "--"})


def overallUnemploymentTrend():
    print("Plotting 1/7: Overall unemployment rate...")
    fig, ax = plt.subplots(figsize=(14, 5))
    shade_recessions(ax)
    ax.plot(df.index, df["overall_rate"], color="#1f77b4", linewidth=1.2)
    ax.axhline(df["overall_rate"].mean(), color="gray", linestyle="--", linewidth=0.8,
           label=f"Mean ({df['overall_rate'].mean():.1f}%)")
    ax.set_title("US Unemployment Rate (1948–2024)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Unemployment Rate (%)")
    rec_patch = mpatches.Patch(color="#d9e8f5", label="Recession")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles + [rec_patch], labels + ["Recession"], fontsize=9)
    plt.tight_layout()
    plt.savefig("figures/1_overall_rate.png", dpi=150, bbox_inches="tight")
    plt.close()

def groups_over_time():
    print("Plotting 2/7: Age group trends...")
    fig, ax = plt.subplots(figsize=(14, 6))
    shade_recessions(ax)
    palette = sns.color_palette("tab10", n_colors=len(age_groups))
    for (col, name), color in zip(age_groups.items(), palette):
        ax.plot(df.index, df[col], label=name, linewidth=0.9, color=color)
    ax.set_title("Unemployment Rate by Age Group (1948–2024)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Unemployment Rate (%)")
    rec_patch = mpatches.Patch(color="#d9e8f5", label="Recession")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles + [rec_patch], labels + ["Recession"], fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig("figures/2_age_groups.png", dpi=150, bbox_inches="tight")
    plt.close()


def YouthVsOverall():
    print("Plotting 3/7: Youth-to-overall ratio...")
    annual = df[["overall_rate", "age_16_19_rate"]].resample("YE").mean()
    annual.index = annual.index.year
    annual["ratio"] = annual["age_16_19_rate"] / annual["overall_rate"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    ax1.plot(annual.index, annual["age_16_19_rate"], color="#d62728", label="16–19")
    ax1.plot(annual.index, annual["overall_rate"], color="#1f77b4", label="Overall")
    ax1.set_ylabel("Unemployment Rate (%)")
    ax1.set_title("Teen vs Overall Unemployment (Annual Average)", fontsize=13, fontweight="bold")
    ax1.legend()

    ax2.plot(annual.index, annual["ratio"], color="#ff7f0e", linewidth=1.3)
    ax2.axhline(annual["ratio"].mean(), color="gray", linestyle="--", linewidth=0.8,
    label=f"Mean ({annual['ratio'].mean():.2f}x)")
    ax2.set_ylabel("Teen / Overall Ratio")
    ax2.set_xlabel("Year")
    ax2.set_title("How Many Times Higher Is Teen Unemployment vs Overall?", fontsize=11)
    ax2.legend()
    plt.tight_layout()
    plt.savefig("figures/3_youth_ratio.png", dpi=150, bbox_inches="tight")
    plt.close()


def CovidEffect():
    print("Plotting 4/7: COVID-19 z-scores...")
    pre_covid = df[df.index < "2020-01-01"]
    apr_2020  = df.loc["2020-04-01"]
    rows = []
    for col, name in age_groups.items():
        mu, sigma = pre_covid[col].mean(), pre_covid[col].std()
        z = (apr_2020[col] - mu) / sigma
        rows.append({"Age Group": name, "Apr 2020 Rate": apr_2020[col], "Z-Score": round(z, 2)})
    outlier_df = pd.DataFrame(rows).sort_values("Z-Score", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#d62728" if z > 5 else "#ff7f0e" for z in outlier_df["Z-Score"]]
    bars = ax.barh(outlier_df["Age Group"], outlier_df["Z-Score"], color=colors, edgecolor="white")
    ax.axvline(3, color="gray", linestyle="--", linewidth=0.8, label="3σ threshold")
    ax.set_xlabel("Standard Deviations from Pre-COVID Mean")
    ax.set_title("COVID-19 Shock: How Extreme Was April 2020 for Each Age Group?",
             fontsize=12, fontweight="bold")
    for bar, val in zip(bars, outlier_df["Z-Score"]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
            f"{val}σ", va="center", fontsize=9)
    ax.legend()
    plt.tight_layout()
    plt.savefig("figures/4_covid_shock.png", dpi=150, bbox_inches="tight")
    plt.close()

def SeasonalityTrends():
    print("Plotting 5/7: Seasonal patterns...")
    df_freq = df.asfreq("MS")
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    fig, ax = plt.subplots(figsize=(12, 5))
    for (col, name), color in zip(age_groups.items(), palette):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            decomp = sm.tsa.seasonal_decompose(df_freq[col].dropna(), model="additive", period=12)
        seasonal = decomp.seasonal
        monthly_avg = seasonal.groupby(seasonal.index.month).mean()
        ax.plot(range(1, 13), monthly_avg.values, marker="o", markersize=4,
                label=name, color=color, linewidth=1.2)
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_labels)
    ax.set_ylabel("Seasonal Effect (percentage points)")
    ax.set_title("Seasonal Unemployment Pattern by Age Group\n(Average across all years)",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig("figures/5_seasonality.png", dpi=150, bbox_inches="tight")
    plt.close()

def correlation():
    print("Plotting 6/7: Correlation heatmap...")
    corr_df = df[list(age_groups.keys())].copy()
    corr_df.columns = list(age_groups.values())

    fig, ax = plt.subplots(figsize=(9, 7))
    import numpy as np
    mask = np.triu(np.ones_like(corr_df.corr(), dtype=bool))
    sns.heatmap(corr_df.corr(), mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Between Age Group Unemployment Rates",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("figures/6_correlation.png", dpi=150, bbox_inches="tight")
    plt.close()


def DecadeAverages():
    print("Plotting 7/7: Decade summary...")
    df2 = df.copy()
    df2["decade"] = (df2.index.year // 10) * 10
    decade_df = df2.groupby("decade")[list(age_groups.keys()) + ["overall_rate"]].mean().round(1)
    decade_df.columns = list(age_groups.values()) + ["Overall"]
    decade_df = decade_df[["Overall"] + list(age_groups.values())]

    fig, ax = plt.subplots(figsize=(13, 5))
    sns.heatmap(decade_df.T, annot=True, fmt=".1f", cmap="YlOrRd",
                linewidths=0.5, ax=ax, cbar_kws={"label": "Avg Unemployment Rate (%)"})
    ax.set_xlabel("Decade")
    ax.set_title("Average Unemployment Rate by Decade and Age Group",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("figures/7_decades.png", dpi=150, bbox_inches="tight")
    plt.close()



# ── Module-level computations for KEY FINDINGS ─────────────────────────────────
pre_covid = df[df.index < "2020-01-01"]
annual = df[["overall_rate", "age_16_19_rate"]].resample("YE").mean()
annual.index = annual.index.year
annual["ratio"] = annual["age_16_19_rate"] / annual["overall_rate"]

apr_2020 = df.loc["2020-04-01"]
rows = []
for col, name in age_groups.items():
    mu, sigma = pre_covid[col].mean(), pre_covid[col].std()
    z = (apr_2020[col] - mu) / sigma
    rows.append({"Age Group": name, "Apr 2020 Rate": apr_2020[col], "Z-Score": round(z, 2)})
outlier_df = pd.DataFrame(rows).sort_values("Z-Score", ascending=False)

print("\n========== KEY FINDINGS ==========")
print(f"Overall mean:  {df['overall_rate'].mean():.2f}%")
print(f"All-time high: {df['overall_rate'].max():.1f}% ({df['overall_rate'].idxmax().strftime('%b %Y')})")
print(f"All-time low:  {df['overall_rate'].min():.1f}% ({df['overall_rate'].idxmin().strftime('%b %Y')})")
print(f"Teen multiplier (avg): {annual['ratio'].mean():.2f}x the overall rate")
print("\nCOVID shock severity (Apr 2020):")
print(outlier_df[["Age Group", "Apr 2020 Rate", "Z-Score"]].to_string(index=False))
print("\nAll figures saved to figures/" )