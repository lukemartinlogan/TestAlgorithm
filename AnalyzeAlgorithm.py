
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


def CompareBinStrategies1():
	
	"""
	This function will test if there is
	a significant difference between the
	binning strategies for an interval of
	5 seconds.
	"""
	
	int5 = pd.read_csv("Datasets/results.csv")
	
	#Open dataframe for 5 seconds/old bins
	int5_old = int5[
		(int5["loc_alg"] == 2) & 
		(int5["bin_strat"] == 2) & 
		(int5["building_true"] == 31) & 
		(int5["interval"]==10)  &
		(int5["xy_error"]<=17)
	]
	
	#Open dataframe for 5 seconds/new bins
	int5_new = int5[
		(int5["loc_alg"] == 2) & 
		(int5["bin_strat"] == 7) & 
		(int5["building_true"] == 31) & 
		(int5["interval"]==10) &
		(int5["xy_error"]<=17)
	]
	
	err1 = int5_old["xy_error"]
	err2 = int5_new["xy_error"]
	
	#Error statistics
	error_stats(err1)
	error_stats(err2)
	
	#Show error histograms
	#error_hist(err1)
	#error_hist(err2)
	
	#Show paired t tests
	paired_error_ttest(err1, err2)

def CompareBinStrategies2():
	
	"""
	This function will test if there is
	a significant difference between the
	binning strategies for an interval of
	5 seconds.
	"""
	
	int10 = pd.read_csv("Datasets/results_SB_10s.csv")
	
	#Open dataframe for 10 seconds/old bins
	int10_old = int10[
		(int10["loc_alg"] == 2) & 
		(int10["bin_strat"] == 2) & 
		(int10["building_true"] == 31) & 
		(int10["interval"]==10) #&
		#(int10["xy_error"]<=17)
	]
	
	#Open dataframe for 10 seconds/new bins
	int10_new = int10[
		(int10["loc_alg"] == 2) & 
		(int10["bin_strat"] == 7) & 
		(int10["building_true"] == 31) & 
		(int10["interval"]==10) &
		(int10["xy_error"]<=17)
	]
	
	err1 = int10_old["xy_error"]
	err2 = int10_new["xy_error"]
	
	#Error statistics
	error_stats(err1)
	error_stats(err2)
	
	#Show error histograms
	error_hist(err1, "Visualizations/SB_err10s_old.png", "Distribution of Error (10s Scan, Unoptimized)")
	error_hist(err2, "Visualizations/SB_err10s_new.png", "Distribution of Error (10s Scan, Optimized)")
	
	#Show paired t tests
	#paired_error_ttest(err1, err2)

def CompareScanningPeriods():

	"""
	This function will test if there is a
	significant difference between the
	test distributions.
	"""
	
	#Open dataframe for 5/10 seconds
	int5 = pd.read_csv("Datasets/results_SB_5s.csv")
	int10 = pd.read_csv("Datasets/results_SB_10s.csv")
	
	#Filter 5s
	int5 = int5[
		(int5["loc_alg"] == 2) & 
		(int5["bin_strat"] == 6) & 
		(int5["building_true"] == 31) & 
		(int5["interval"]==5) &
		(int5["xy_error"]<=17)
	]
	
	#Filter 10s
	int10 = int10[
		(int10["loc_alg"] == 2) & 
		(int10["bin_strat"] == 7) & 
		(int10["building_true"] == 31) & 
		(int10["interval"]==10) &
		(int10["xy_error"]<=17)
	]
	
	#Use 10 second bin strategy
	err1 = int5["xy_error"]
	err2 = int10["xy_error"]
	
	#Compute error statistics
	error_stats(err1)
	error_stats(err2)
	
	#Show error histograms
	#error_hist(err1, "Visualizations/SB_err_5s.png", "Distribution of Error (5s Scan)")
	#error_hist(err2, "Visualizations/SB_err10s.png", "Distribution of Error (10s Scan)")

def main():

	CompareBinStrategies2() 
	
if __name__ == "__main__":
	main()
	
	
	
	
