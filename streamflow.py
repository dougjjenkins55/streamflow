from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


def load_streamflow(filename):
    """Read the streamflow CSV. Return the dates and a 2D array of flows (cfs), one column per gauge."""
    data = np.genfromtxt(filename, delimiter=",", dtype=str, skip_header=1)
    dates = data[:, 0].astype("datetime64[m]")
    flows = data[:, 1:].astype(float)
    return dates, flows


def plot_streamflow(dates, flows, sites):
    """Plot the flow at each gauge, with the same title, labels, and formatting as the Matplotlib HW."""
    colors = ["purple", "teal", "green", "orange", "orangered"]

    plt.figure(figsize=(6, 5), facecolor="white")

    for column, (site, color) in enumerate(zip(sites, colors)):
        plt.plot(
            dates,
            flows[:, column],
            color=color,
            label=site,
            linewidth=1.2,
        )

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


if __name__ == "__main__":
    sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
    csv_path = Path(__file__).resolve().parent / "June-2021-Provo-River-Streamflow-Rates.csv"
    dates, flows = load_streamflow(csv_path)
    plot_streamflow(dates, flows, sites)

