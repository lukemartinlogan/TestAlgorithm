
import sys
import math, numpy as np
import random
import pandas as pd
from progressbar import ProgressBar
from Algorithms import *
from TestData import *
from TestAlgorithm import *

def rand_bin_rssis(bins, fix_rssi_width=False, max_rssi=-65, rssi_width_range=(10, 30)):

	"""
	Randomly generate the rssi mapping while keeping distances the same

	[(r1+r2+r3+r4, d4), (r1+r2+r3, d3), (r1+r2, d2), (r1, d1)]
	"""

	num_bins = len(bins)
	if fix_rssi_width:
		rssi_widths = [max_rssi] + [-random.randint(rssi_width_range[0], rssi_width_range[1])]*(num_bins-1)
	else:
		rssi_widths = [max_rssi] + [-random.randint(rssi_width_range[0], rssi_width_range[1]) for i in range(num_bins-1)]

	rssi = 0
	dist = 0
	new_bins = []
	for i in range(num_bins):
		rssi += rssi_widths[i]
		dist = bins[num_bins - i - 1][1]
		new_bins.insert(0, [rssi, dist])

	return new_bins

def rand_bin_dists(bins, fix_dist_width=False, min_dist=1, dist_width_range=(1, 10)):

	"""
	Randomly generate the distance mapping while keeping RSSIs the same
	"""

	num_bins = len(bins)
	if fix_dist_width:
		dist_widths = [min_dist] + [random.randint(dist_width_range[0]*2, dist_width_range[1])/2]*(num_bins - 1)
	else:
		dist_widths = [min_dist] + [random.randint(dist_width_range[0]*2, dist_width_range[1])/2 for i in range(num_bins-1)]

	rssi = 0
	dist = 0
	new_bins = []
	for i in range(num_bins):
		rssi = bins[num_bins - i - 1][0]
		dist += dist_widths[i]
		new_bins.insert(0, [rssi, dist])

	return new_bins

def rand_bin(
	num_bins, fix_dist_width=False, fix_rssi_width=False,
	max_rssi=-65, rssi_width_range=(10,30),
	min_dist=1, dist_width_range=(1,10)
):

	"""
	Randomly generate a bin strategy
	"""

	if fix_rssi_width:
		rssi_widths = [max_rssi] + [-random.randint(rssi_width_range[0], rssi_width_range[1])]*(num_bins-1)
	else:
		rssi_widths = [max_rssi] + [-random.randint(rssi_width_range[0], rssi_width_range[1]) for i in range(num_bins-1)]
	if fix_dist_width:
		dist_widths = [min_dist] + [random.randint(dist_width_range[0]*2, dist_width_range[1]*2)/2]*(num_bins - 1)
	else:
		dist_widths = [min_dist] + [random.randint(dist_width_range[0]*2, dist_width_range[1]*2)/2 for i in range(num_bins-1)]

	rssi = 0
	dist = 0
	new_bins = []
	for i in range(num_bins):
		rssi += rssi_widths[i]
		dist += dist_widths[i]
		new_bins.insert(0, [rssi, dist])

	return new_bins

class BinOptimizer:

	def __init__(self, cases = None):

		self.bins = None
		self.xy_error = np.inf
		self.floor_error = np.inf
		self.cases = cases

	def set_cases(self, cases):
		self.cases = cases

	def reset(self):
		self.bins = None
		self.error = np.inf

	def optimize_fixed_rssi(
		self, bins, loc_alg, floor_alg, top_n=3,
		min_dist = 1, dist_width_range = (1,10),
		fix_dist_width = False,
		num_guesses = 50, max_iter=0, tol=.001
	):

		"""
		Finds the best distances for the given RSSI bins
		Fixes RSSI and varies distances.

		bins: The initial bin guess
		min_dist: The minimum distance a user can be standing from a beacon
		max_dist: The maximum distance a user can be standing from a beacon
		fix_rssi_width: Whether or not to create different bin widths for RSSI mappings
		num_guesses: The number of distance mappings to make
		max_iter: The number of iterations to make in the gradient descent
		tol: The minimum difference between two error measurements to stop iterating
		"""

		pbar = ProgressBar()
		bins = bin_strategies[bins]
		for i in pbar(range(num_guesses)):
			bin_strategies[-1] = bins
			self.cases.test_algorithm(loc_alg, floor_alg, -1, top_n, to_csv=False)
			if self.cases.net_floor_error <= self.floor_error:
				if self.cases.net_floor_error < self.floor_error:
					self.bins = bins
					self.xy_error = self.cases.net_xy_error
					self.floor_error = self.cases.net_floor_error
				elif self.cases.net_xy_error < self.xy_error:
					self.bins = bins
					self.xy_error = self.cases.net_xy_error
					self.floor_error = self.cases.net_floor_error
			bins = rand_bin_dists(bins, fix_dist_width, min_dist, dist_width_range)

	def optimize_fixed_dist(
		self, bins, loc_alg, floor_alg, top_n=3,
		max_rssi = -65, rssi_width_range = (10,30),
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

		bins = bin_strategies[bins]
		pbar = ProgressBar()
		for i in pbar(range(num_guesses)):
			bin_strategies[-1] = bins
			self.cases.test_algorithm(loc_alg, floor_alg, -1, top_n, to_csv=False)
			if self.cases.net_floor_error <= self.floor_error:
				if self.cases.net_floor_error < self.floor_error:
					self.bins = bins
					self.xy_error = self.cases.net_xy_error
					self.floor_error = self.cases.net_floor_error
				elif self.cases.net_xy_error < self.xy_error:
					self.bins = bins
					self.xy_error = self.cases.net_xy_error
					self.floor_error = self.cases.net_floor_error
			bins = rand_bin_rssis(bins, fix_rssi_width, max_rssi, rssi_width_range)

	def optimize_full(
		self, bins, loc_alg, floor_alg, top_n=3,
		max_rssi = -65, rssi_width_range = (10,30),
		min_dist = 1, dist_width_range = (1,10),
		fix_dist_width = False, fix_rssi_width=False,
		num_guesses = 50, max_iter=0, tol=.001
	):
		"""
		Determines the optimal binning strategy for a given dataset.
		Varies dist and rssi.

		"""

		bins = bin_strategies[bins]
		pbar = ProgressBar()
		for i in pbar(range(num_guesses)):
			bin_strategies[-1] = bins
			self.cases.test_algorithm(loc_alg, floor_alg, -1, top_n, to_csv=False)
			if self.cases.net_floor_error <= self.floor_error:
				if self.cases.net_floor_error < self.floor_error:
					self.bins = bins
					self.xy_error = self.cases.net_xy_error
					self.floor_error = self.cases.net_floor_error
				elif self.cases.net_xy_error < self.xy_error:
					self.bins = bins
					self.xy_error = self.cases.net_xy_error
					self.floor_error = self.cases.net_floor_error
			bins = rand_bin(
				len(bins), fix_dist_width, fix_rssi_width,
				max_rssi, rssi_width_range,
				min_dist, dist_width_range)

	def __str__(self):

		string = ""
		string += "Total XY Error: " + str(self.xy_error) + "\n"
		string += "Total Floor Error: " + str(self.floor_error) + "\n"
		string += "Bin Strategy: " + str(self.bins) + "\n"
		return string
