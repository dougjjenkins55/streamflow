# -*- coding: utf-8 -*-

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Load and graph the Provo River streamflow data for June 2021.
csv_path = Path(__file__).resolve().parent / "June-2021-Provo-River-Streamflow-Rates.csv"
data = np.genfromtxt(csv_path, delimiter=",", dtype=str, skip_header=1)

x = data[:, 0]
y_1 = data[:, 1].astype(float)
y_2 = data[:, 2].astype(float)
y_3 = data[:, 3].astype(float)
y_4 = data[:, 4].astype(float)
y_5 = data[:, 5].astype(float)

x_datetime = pd.to_datetime(x)

plt.figure(figsize=(6, 5), facecolor="white")

plt.plot(x_datetime, y_1, color="purple", label="10163000", linewidth=1.2)
plt.plot(x_datetime, y_2, color="teal", label="10155200", linewidth=1.2)
plt.plot(x_datetime, y_3, color="green", label="10155500", linewidth=1.2)
plt.plot(x_datetime, y_4, color="orange", label="10154200", linewidth=1.2)
plt.plot(x_datetime, y_5, color="orangered", label="10155000", linewidth=1.2)

plt.title("Provo River Streamflow Data (2021)")
plt.xlabel("Date")
plt.ylabel("Flowrate (cfs)")
plt.legend(title="Site Numbers", loc="upper right")
plt.grid(True, linestyle="-", linewidth=0.5, alpha=0.7)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.gcf().autofmt_xdate()

plt.tight_layout()
plt.show()

