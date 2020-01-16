
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
	
	n, bins, patches = plt.hist(error, facecolor='blue')
	plt.xlabel("Error (meters)")
	plt.ylabel("Count")
	plt.title(title)
	plt.savefig(out)
	plt.close()

def ViewStats(df, bin_strat, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10):
	
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
	

def CompareBinStrategies(
	bin_strat1, bin_strat2, loc_alg=2, floor_alg=1, top_n=3, building="SB", interval=10, 
	hist1_out="Visualizations/ErrorHist1.png",  hist2_out="Visualizations/ErrorHist2.png",
	hist1_title="Distribution of Error 1",  hist2_title="Distribution of Error 2",
	dataset="Datasets/results.csv"
):
	
	"""
	Test if there is a significant difference
	between two binning strategies in a particular
	building.
	"""
	
	res = pd.read_csv(dataset)
	
	#Open dataframe for strategy 1
	res1= res[
		(res["loc_alg"] == loc_alg) & 
		(res["bin_strat"] == bin_strat1) & 
		(res["building_true"] == BuildingStrToCode[building]) & 
		(res["interval"] == interval)  &
		(res["top_n"] == top_n)
	]
	
	#Open dataframe for strategy 2
	res2 = res[
		(res["loc_alg"] == loc_alg) & 
		(res["bin_strat"] == bin_strat2) & 
		(res["building_true"] == BuildingStrToCode[building]) & 
		(res["interval"] == interval)  &
		(res["top_n"] == top_n)
	]
	
	#Get error distributions
	err1 = res1["xy_error"]
	err2 = res2["xy_error"]
	
	#Error statistics
	error_stats(err1)
	error_stats(err2)
	
	#Show error histograms
	error_hist(err1, out=hist1_out, title=hist1_title)
	error_hist(err2, out=hist2_out, title=hist2_title)
	
	#Show paired t tests
	#paired_error_ttest(err1, err2)

def CompareScanningPeriods(
	int1, int2, bin_strat=1, loc_alg=2, floor_alg=1, top_n=3, building="SB",
	hist1_out="Visualizations/ErrorHist1.png",  hist2_out="Visualizations/ErrorHist2.png",
	hist1_title="Distribution of Error 1",  hist2_title="Distribution of Error 2",
	dataset="Datasets/results.csv"
):

	"""
	Test if there is a significant difference
	between two scanning periods for a
	particular building and bin strategy.
	"""
	
	res = pd.read_csv(dataset)
	
	#Open dataframe for first interval
	res1= res[
		(res["loc_alg"] == loc_alg) & 
		(res["bin_strat"] == bin_strat) & 
		(res["building_true"] == BuildingStrToCode[building]) & 
		(res["interval"] == int1)  &
		(res["top_n"] == top_n)  &
		(res["xy_error"]<=17)
	]
	
	#Open dataframe for second interval
	res2 = res[
		(res["loc_alg"] == loc_alg) & 
		(res["bin_strat"] == bin_strat) & 
		(res["building_true"] == BuildingStrToCode[building]) & 
		(res["interval"] == int2) &
		(res["top_n"] == top_n) &
		(res["xy_error"]<=17)
	]
	
	#Get error distributions
	err1 = res1["xy_error"]
	err2 = res2["xy_error"]
	
	#Error statistics
	error_stats(err1)
	error_stats(err2)
	
	#Show error histograms
	error_hist(err1, out=hist1_out, title=hist1_title)
	error_hist(err2, out=hist2_out, title=hist2_title)
	
	#Show paired t tests
	#paired_error_ttest(err1, err2)
	#paired_error_ttest(err1, err2)

	
	
	
