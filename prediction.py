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

df = pd.read_csv("employment.csv", parse_dates=["date"])
df = df.sort_values("date").set_index("date")
df = df.asfreq("MS")

series = df["overall_rate"]   # ← add this line     

#We will split the dataset into train and test
# normal economical conditions will be 1948-2019 inclusive
# testing on an outlying condition namely covid is 2020-2024

train = series.loc[:"2019-12-01"]
test  = series.loc["2020-01-01":]
print(f"Training on {len(train)} months (Jan 1948 – Dec 2019)")
print(f"Testing on  {len(test)} months (Jan 2020 – present)")

#We will fit the sarima model to the included data

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model = sm.tsa.SARIMAX(
        train,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    result = model.fit(disp=False)

print("Completed Model Fitting")
print(f"\nModel summary stats:")
print(f"  AIC:  {result.aic:.2f}  (lower = better fit)")
print(f"  BIC:  {result.bic:.2f}  (lower = better fit)")

#forecasting over covid timeframe
forecast_obj = result.get_forecast(steps = len(test))
forecast = forecast_obj.predicted_mean
ci = forecast_obj.conf_int(alpha=0.05)
ci.columns = ["lower","upper"]

pre_covid_test = test.loc[:"2020-02-01"]
pre_covid_pred = forecast.loc[:"2020-02-01"]

mae = np.mean(np.abs(pre_covid_test.values - pre_covid_pred.values))
rmse = np.sqrt(np.mean((pre_covid_test.values - pre_covid_pred.values)**2))

print(f"mae = {mae} and rmse = {rmse}")
