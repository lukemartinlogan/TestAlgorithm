
from TestData import *
from TestAlgorithm import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime

def error_stats(error):

	"""
	This function will compute some statistics about
	the error produced by an algorithm.
	"""
	
	mean = np.mean(error)
	stddev = np.std(error)
	
	print("n: ", len(error))
	print("Mean: " + str(mean))
	print("Standard Deviation: " + str(stddev))
	print()


def paired_error_ttest(err1, err2):

	"""
	This function will determine if there is a
	significant difference between the two
	populations.
	"""
	
	error_hist(err1-err2)
	(t, p) = stats.ttest_rel(err1, err2)
	
	print("Probability there is no difference: " + str(p))


def error_hist(error, out="figure.png", title="figure"):

	"""
	This function will show a histogram of error
	for the results of the algorithm.
	"""
	
	n, bins, patches = plt.hist(error, facecolor='blue', range=(0, 14), bins=10)
	plt.xlabel("Error (meters)")
	plt.ylabel("Count")
	plt.title(title)
	plt.savefig(out)
	plt.close()

def ViewStats(df, bin_strat, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, hist_title="figure", hist_out="figure.png"):
	
	"""
	Viewing stats about particular test environment.
	"""
	
	res1= df[
		(df["loc_alg"] == loc_alg) & 
		(df["bin_strat"] == bin_strat) & 
		(df["building_true"] == BuildingStrToCode[building]) & 
		(df["interval"] == interval)  &
		(df["top_n"] == top_n)
	]
	err1 = res1["xy_error"]
	error_stats(err1)
	error_hist(err1, title=hist_title, out=hist_out)
	
