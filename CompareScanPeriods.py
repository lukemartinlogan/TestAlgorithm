
"""
This file will be used to compare the error
produced by different scanning periods.

1. Draw a histogram of the error rate for a scan period
2. Estimate the parameters for gamma distribution for a scan period
3. Compare each scan period with another
"""

import pandas as pd
import matplotlib.pyplot as plt

def DrawIntervalHistogram(df, interval):
	df = df[df["interval"] == interval]
	n, bins, patches = plt.hist(df["xy_error"], facecolor="blue")
	plt.xlabel('Error')
	plt.ylabel('Count')
	plt.title("Histogram of Error for Interval of {:d} Seconds".format(interval))
	plt.savefig("hist-{:d}.png".format(interval))
	plt.close()

def main():
	df = pd.read_csv("./sim_results.csv")
	DrawIntervalHistogram(df, 2)
	DrawIntervalHistogram(df, 3)
	DrawIntervalHistogram(df, 5)
	DrawIntervalHistogram(df, 10)

if __name__ == "__main__":
	main()