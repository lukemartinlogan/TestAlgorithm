
import sys
import math, numpy as np
import random
import pandas as pd
from numba import njit, prange
from Algorithms import *
from TestData import *
from TestAlgorithm import *

"""
A genetic algorithm for finding the optimal bins
sizes.
"""

class Bins:
	
	def __init__(self, num_bins):
	
		"""
		Keeps track of RSSI to distance
		mappings.
		
		num_bins: The number of bins to create
		bin_min: The minimum signal strength to consider
		bin_max: The maximum signal strength to consider
		"""
		
		self.num_bins = num_bins
		self.bins = None
		self.dist = None
		self.rssi = None
	
	def set_bins(self, bins):
		self.bins = bins
		self.num_bins = len(bins)
	
	def rand_bin_rssis(self, fix_rssi_width=False, max_rssi=-65, rssi_width_range=(10, 30)):
		
		"""
		Randomly generate the rssi mapping while keeping distances the same
		
		[(r1+r2+r3+r4, d4), (r1+r2+r3, d3), (r1+r2, d2), (r1, d1)
		"""
		
		self.rssi = [max_rssi] + [-random.randint(rssi_width_range) for i in range(self.num_bins-1)]
		self.bins = []
		self.score = np.inf
		
		rssi = 0
		dist = 0
		self.bins = []
		for i in range(self.num_bins): 
			rssi += self.rssi[i]
			dist += self.dist[i]
			self.bins.insert(0, [rssi, dist])
		
		
	def rand_bin_dists(self, fix_dist_width=False, min_dist=1, dist_width_range=(1, 10)):
		
		"""
		Randomly generate the distance mapping while keeping RSSIs the same
		"""
		
				
	def rand_bin(
		self, num_bins, fix_dist_width=False, fix_rssi_width=False, 
		max_rssi=-65, rssi_width_range=(10,30),
		min_dist=1, dist_width_range=(1,10)
	):
		
		"""
		Randomly generate a bin
		"""
		
		self.num_bins = num_bins
		self.rssi = [0] + [random.randint(-70, -10) for i in range(self.num_bins-1)]
		self.dist = [random.randint(1, 10) for i in range(num_bins)]
		self.bins = []
		self.score = np.inf
		
		rssi = 0
		dist = 0
		self.bins = []
		for i in range(self.num_bins):
			
			rssi += self.rssi[i]
			dist += self.dist[i]
			self.bins.insert(0, [rssi, dist])
	
	def __str__(self):
		
		return str(self.score)
		

class BinOptimizer:

	def __init__(self):
		
		self.bins = None
		self.error = 0
		self.cases = None

	
	def open_test_data(self, path = "database.csv", building = None, floor = None, sample=None, interval=None):
		
		self.cases = TestCases()
		self.cases.open_test_data(path, building, floor, sample, interval)
	
	def optimize_fixed_rssi(
		self, bins, loc_alg, floor_alg, top_n=3,
		min_dist = 1, max_dist = 15,
		fix_dist_width = False,
		num_guesses = 50, max_iter=0, tol=.001
	):
		
		"""
		Determines the optimal binning strategy for a given dataset.
		Fixes RSSI and varies distances.
		
		bins: The initial bin guess
		min_dist: The minimum distance a user can be standing from a beacon
		max_dist: The maximum distance a user can be standing from a beacon
		fix_rssi_width: Whether or not to create different bin widths for RSSI mappings
		num_guesses: The number of distance mappings to make
		max_iter: The number of iterations to make in the gradient descent
		tol: The minimum difference between two error measurements to stop iterating
		"""
		
		return
	
	def optimize_fixed_dist(
		self, bins, loc_alg, floor_alg, top_n=3,
		min_rssi = -110, max_rssi = -65,
		fix_rssi_width=False,
		num_guesses = 50, max_iter=0, tol=.001
	):
		"""
		Determines the optimal binning strategy for a given dataset.
		Fixes dist and varies RSSI.
		
		bins: The initial bin guess
		min_dist: The minimum distance a user can be standing from a beacon
		max_dist: The maximum distance a user can be standing from a beacon
		fix_rssi_width: Whether or not to create different bin widths for RSSI mappings
		num_guesses: The number of RSSI mappings to make
		max_iter: The number of iterations to make in the gradient descent
		tol: The minimum difference between two error measurements to stop iterating
		"""
	
		return
	
	def optimize_full(
		self, loc_alg, floor_alg, top_n=3, num_bins = 4,
		max_rssi = -65,
		min_dist = 1, max_dist = 15,
		fix_dist_width=False,
		fix_rssi_width=False,
		num_start_guesses=50, num_part_guesses=10, max_iter=0, tol=.001
	):
		
		"""
		Determines the optimal binning strategy for a given dataset.
		Varies all of the bin widths.
		
		loc_alg: The location algorithm ID in the loc_algorithms dict in Algorithms.py
		floor_alg: The floor algorithm ID in the floor_algorithms dict in Algorithms.py
		top_n: The number of signal strengths to consider in the location computation
		num_bins: The number of bins to optimize for
		min_rssi: The minimum possible RSSI
		max_rssi: The maximum possible RSSI
		min_dist: The minimum distance a user can be standing from a beacon
		max_dist: The maximum distance a user can be standing from a beacon
		fix_dist_width: Whether or not to create different bin widths for distance mappings
		fix_rssi_width: Whether or not to create different bin widths for RSSI mappings
		num_start_guesses: The number of places to start the 
		num_part_guesses: The number of places to start in the partial optimizers
		max_iter: The number of iterations to make in the gradient descent
		tol: The minimum difference between two error measurements to stop iterating
		"""
		
		#Generate initial bin guesses
    
		return
    
	def __str__(self):

		string = ""
		string += "Total Error: " + str(self.error) + "\n"
		string += "Bin Strategy: " + str(self.bins) + "\n"
		return string
	
