# US Unemployment Time-Series Analysis (1948–2024)

Exploratory data analysis on 76 years of monthly US unemployment data, broken down by age group. The project looks at long-run trends, how recessions hit different generations, the COVID-19 shock, seasonal patterns, and decade-by-decade comparisons.

> **Data source:** Data for this dataset is sourced directly from the Federal Reserve Economic Data (FRED) API. FRED provides a wealth of economic data and financial indicators, and is a primary source of economic data in the U.S.


---

## Project Structure

```
unemployment-analysis/
├── employment.csv    # The raw data
├── analysis.py       # All the analysis and charts — run this
├── figures/          # All generated charts (created automatically)
└── README.md
```

---

## How to Run

```bash
# Install dependencies (only needed once)
pip install pandas matplotlib seaborn statsmodels scipy

# Run the analysis — generates all charts into figures/
python analysis.py
```

---

## Charts Generated

| File | What it shows |
|------|---------------|
| `1_overall_rate.png` | Overall US unemployment 1948–2024 with recession shading |
| `2_age_groups.png` | All age groups overlaid on the same chart |
| `3_youth_ratio.png` | How many times higher teen unemployment is vs the overall rate |
| `4_covid_shock.png` | How extreme April 2020 was for each age group (z-scores) |
| `5_seasonality.png` | Recurring seasonal patterns by age group |
| `6_correlation.png` | How closely each age group moves together |
| `7_decades.png` | Average unemployment by decade and age group |

---

## Key Findings

**Teen unemployment runs about 3× the overall rate, always.**
The 16–19 age group has averaged 16.0% since 1948 — roughly 2.86× the overall rate of 5.69%. This gap isn't fixed though; it was widest in the late 1960s (3.52×) and narrowed during COVID recovery (2.19×).

**COVID-19 was the largest shock in 76 years — and hit older workers hardest in relative terms.**
April 2020 pushed the overall rate to 14.8%, the highest on record. But measured against each group's normal range, workers 55+ experienced the most extreme spike (9.1 standard deviations above their pre-COVID average), while teens — despite hitting 32.8% — were less statistically unusual because teen unemployment is always volatile.

| Age Group | Apr 2020 Rate | How extreme (σ) |
|-----------|--------------|-----------------|
| 55+       | 13.6%        | 9.1σ |
| 45–54     | 12.3%        | 6.8σ |
| 20–24     | 25.5%        | 6.3σ |
| Overall   | 14.8%        | 5.5σ |
| 16–19     | 32.8%        | 4.3σ |

**The 1980s were the worst decade across every age group.**
The back-to-back recessions of 1980 and 1981–82 created a sustained labour market depression. Overall unemployment averaged 7.3% for the decade — the highest of any decade in the dataset.

**All age groups move together, but the levels are very different.**
Correlation between age groups is extremely high (all pairs r > 0.94), meaning recessions and recoveries hit everyone in the same direction. But the absolute rates differ enormously — teens at 16% average vs. workers 45–54 at just 3.8%.

**Seasonality is consistent but small.**
Teen unemployment peaks every June as school-leavers enter the job market, then troughs in December. Most other groups peak in April–May and recover through the summer. The swings are only around 0.1–0.3 percentage points.

---

## Context

This project examines how political tensions, economic policy shifts, and exogenous shocks — from the post-war boom to Vietnam-era stagflation, the Volcker rate hikes of the 1980s, and COVID-19 — ripple differently through the age structure of the US labour force.