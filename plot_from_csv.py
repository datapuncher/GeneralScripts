#!/usr/bin/python

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read CSV and parse datetime column
df = pd.read_csv(
    "Book1.csv",
    parse_dates=["datetime"]
)

# Create figure
fig, ax = plt.subplots(figsize=(9, 4))

# Plot data: green dotted line
ax.plot(
    df["datetime"],
    df["value"],
    linestyle=":",      # dotted line
    color="green",      # green color
    marker="o",         # optional: makes points clearer
    linewidth=2
)

# Format x-axis: date + time (stacked)
ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%Y-%m-%d\n%H:%M")
)

# Labels
ax.set_xlabel("Date and Time")
ax.set_ylabel("Value")

# Automatically rotate and align labels
fig.autofmt_xdate()

plt.tight_layout()
plt.show()

