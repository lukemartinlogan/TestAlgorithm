
from TestData import *
from TestAlgorithm import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def signal_stats(sig):

	"""
	This function will compute some statistics about
	the error produced by an algorithm.
	"""
	
	minimum = np.min(sig)
	maximum = np.max(sig)
	mean = np.mean(sig)
	stddev = np.std(sig)
	
	print("n: ", len(sig))
	print("Min: " + str(minimum))
	print("Max: " + str(maximum))
	print("Mean: " + str(mean))
	print("Standard Deviation: " + str(stddev))
	print()

def signal_hist(sig, title="figure", out="figure.png"):

	"""
	This function will show a histogram of error
	for the results of the algorithm.
	"""
	
	n, bins, patches = plt.hist(sig, facecolor='blue')
	plt.xlabel("Signal Stregnth (dBm)")
	plt.ylabel("Count")
	plt.title(title)
	plt.savefig(out)
	plt.close()



def ViewSignalStats(cases, hist_title="Signal Distribution", hist_out="sigdist.png"):
	
	#Load the signal distribution
	sig = []
	for case in cases.test_cases:
		rssis = case.getNearestBeaconsAvgMwToDbm()[4]
		print(len(rssis))
		sig += rssis
	
	#Compute stats
	signal_stats(sig)
	
	#Compute histogram
	signal_hist(sig, hist_title, hist_out)




