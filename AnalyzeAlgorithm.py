
from TestData import *
from TestAlgorithm import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

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


def error_hist(error):

	"""
	This function will show a histogram of error
	for the results of the algorithm.
	"""
	
	n, bins, patches = plt.hist(error, facecolor='blue')
	plt.show()


def CompareBinStrategies():
	
	"""
	This function will test if there is
	a significant difference between the
	binning strategies for an interval of
	5 seconds.
	"""
	
	#Open dataframe for 5 seconds/old bins
	int5_old = pd.read_csv("./results.csv")
	int5_old = int5_old[
		(int5_old["loc_alg"] == 2) & 
		(int5_old["bin_strat"] == 2) & 
		(int5_old["building_true"] == 31) & 
		(int5_old["interval"]==5)
	]
	
	#Open dataframe for 5 seconds/new bins
	int5_new = pd.read_csv("./results_SB_5s.csv")
	
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


def CompareScanningPeriods():

	"""
	This function will test if there is a
	significant difference between the
	test distributions.
	"""
	
	#Open dataframe for 5 seconds
	int5 = pd.read_csv("results_SB_5s.csv")
	int10 = pd.read_csv("results_SB_10s.csv")
	
	#Use 10 second bin strategy
	err1 = int5["xy_error"]
	err2 = int10["xy_error"]

	#Compute error statistics
	error_stats(err1)
	error_stats(err2)
	
	#Show error histograms
	error_hist(err1)
	error_hist(err2)


def main():

	CompareBinStrategies()
	
if __name__ == "__main__":
	main()
	
	
	
	