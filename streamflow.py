import csv
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
    output_path = Path(__file__).resolve().parent / "provo_streamflow.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


# Excel check: for gauge 10163000, the maximum is 131.0 cfs and the average is 57.0 cfs.
def summarize(dates, flows, sites):
    """Find and print each gauge's maximum, minimum, and average flow, then save a CSV summary."""
    rows = []

    print(f"{'Gauge':<12}{'Max (cfs)':>12}{'Date of max':>24}{'Min (cfs)':>12}{'Avg (cfs)':>12}")

    for column, site in enumerate(sites):
        gauge_flow = flows[:, column]
        max_index = np.argmax(gauge_flow)
        max_flow = gauge_flow[max_index]
        max_date = np.datetime_as_string(dates[max_index], unit="m")
        min_flow = np.min(gauge_flow)
        avg_flow = np.mean(gauge_flow)

        print(
            f"{site:<12}{max_flow:>12.1f}{max_date:>24}"
            f"{min_flow:>12.1f}{avg_flow:>12.1f}"
        )
        rows.append([site, f"{max_flow:.1f}", max_date, f"{min_flow:.1f}", f"{avg_flow:.1f}"])

    summary_path = Path(__file__).resolve().parent / "streamflow_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow(["Gauge", "Max (cfs)", "Date of max", "Min (cfs)", "Avg (cfs)"])
        writer.writerows(rows)


if __name__ == "__main__":
    sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
    csv_path = Path(__file__).resolve().parent / "June-2021-Provo-River-Streamflow-Rates.csv"
    dates, flows = load_streamflow(csv_path)
    plot_streamflow(dates, flows, sites)
    summarize(dates, flows, sites)

    threshold = float(input("Enter a flow threshold in cfs: "))

    print("\nHours above threshold:")
    # Each reading represents 15 minutes, or 0.25 hours.
    for column, site in enumerate(sites):
        reading_count = np.sum(flows[:, column] > threshold)
        hours_above = reading_count * 0.25
        print(f"{site}: {hours_above:.2f} hours")

