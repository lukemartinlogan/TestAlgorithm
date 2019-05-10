
import sys
import math, numpy as np
import random
import pandas as pd
from Algorithms import *
from TestData import *
from TestAlgorithm import *

"""
A genetic algorithm for finding the optimal bins
sizes.
"""


class BinOptimizer:

	def __init__(self):
		
		self.bins = None
		self.error = 0
		self.cases = None

	
	def open_test_data(self, path = "database.csv", building = None, floor = None, sample=None, interval=None):
		
		self.cases = TestCases()
		self.cases.open_test_data(path, building, floor, sample, interval)

		
	def initial_population(self, pop_size, num_bins):
		
		"""
		Randomly select a set of binning
		strategies and creates their
		initial scores.
		
		Bin strategies are considered
		"chromosomes".
		"""
		
		pop = [None]*pop_size
		
		for i in range(pop_size):
		
			#RSSI bin widths
			rssi = [0] + [random.randint(-70, -10) for i in range(num_bins-1)]
			
			#Distance bin widths
			distance = [random.randint(1, 10) for i in range(num_bins)]
		
			#Save bin width guesses
			pop[i] = [
				rssi,		#RSSI bin widths
				distance,	#Distance bin widths
				[],			#Bin strategy
				np.inf, 	#Score of this bin strategy
			]
			
		return pop
		
		
	def compute_bins(self, pop, num_bins):

		"""
		This function will compute the bins
		using the bin widths.
		"""
		
		for bins in pop:
			bins[2] = [ [bins[0][0], bins[1][0]] ]
			for i in range(1, num_bins):
				bins[0][i] += bins[0][i-1]
				bins[1][i] += bins[1][i-1]
				bins[2].append([bins[0][i], bins[1][i]])
	
		
	def fitness_scores(self, pop, loc_alg, floor_alg, top_n):
	
		"""
		Computes the fitness of each bin in the current
		population. Fitness is defined to be the total
		error in location estimates produced by this
		bin size.
		"""
		
		#Test the algorithm with this new strategy
		for i in range(len(pop)):
			self.cases.reset()
			self.cases.test_algorithm(loc_alg=loc_alg, floor_alg=floor_alg, bin_strategy=(0, pop[i][2]), top_n=top_n)
			pop[i][3] = self.cases.net_xy_error
			print(pop[i][2])
		print()
	
	
	def selection(self, pop):
	
		"""
		Selects a subset of the current population of
		chromosomes to evolve from. It will select either
		two genes or the top 10% of genes.
		"""
		
		#Sort population by fitness
		pop.sort(key = lambda bins : bins[3])
		
		#Select the top 10%
		if len(pop) * .1 >= 2:
			return pop[0:int(len(pop)*.1)]
		
		#Select the top two
		return pop[0:2]

	
	def crossover(self, pop, pop_size, num_bins):
	
		"""
		Combines different bins using the
		currently best bin strategies to
		form a new population.
		"""
		
		new_pop = pop.copy()
		
		for i in range(pop_size - len(new_pop)):
			
			#Select two random chromosomes
			bins1 = pop[random.randrange(0, len(pop))]
			bins2 = pop[random.randrange(0, len(pop))]
			bins = bins1.copy()
			
			#Change bin widths
			for bin_type in range(2):
				for bin in range(num_bins):
					prob = random.random()
					if prob < .05:
						print(bins1[bin_type][bin])
						print(bins2[bin_type][bin])
						bins[bin_type][bin] = (bins1[bin_type][bin] + bins2[bin_type][bin])/2
						print(bins[bin_type][bin])
						print()
					
			#Add the new bin strategy to the population
			new_pop.append(bins)
			
		return new_pop
	
	
	def mutate(self, pop, num_bins):
		
		"""
		This function will randomly change
		some of the bins in the population.
		"""
		
		for bins in pop:
			
			#Generate probability
			prob = random.random()
			
			#Replace some bins
			if prob < .05:
				for i in range(num_bins):
					
					#Generate probability
					prob = random.random()
					
					#Change the bin widths
					if prob < .05:
						bins[0][i] = random.randint(-70, -10)
						bins[1][i] = random.randint(1, 10)

		
	def get_fittest(self, pop):
		
		for bins in pop:
			if bins[3] < self.error:
				self.error = bins[3]
				self.bins = bins[2]
	
	
	def optimize(self, loc_alg, floor_alg, top_n=3, num_bins = 4, pop_size = 50, num_generations = 100):
	
		"""
		A genetic algorithm for finding the optimal bin
		sizes for a given set of test data. 
		
		loc_alg: a tuple of the following form: (id, loc_algorithm_model)
		floor_alg: a tuple of the following form: (id, floor_algorithm_model)
		top_n: The number of beacons to consider when computing location
		num_bins: The number of bins per step function
		pop_size: The number of bins to evolve
		num_generations: The maximum number of times evolution occurs
		"""
		
		#Reset optimizer metadata
		self.error = np.inf
		self.bins = None
		self.cases.reset()
		
		#Create the initial population
		pop = self.initial_population(pop_size, num_bins)
		self.compute_bins(pop, num_bins)
		self.fitness_scores(pop, loc_alg, floor_alg, top_n)
		
		#Evolve population
		for i in range(num_generations):
			sys.stdout.write(str((i+1)/num_generations) + "\r")
			pop = self.selection(pop)
			pop = self.crossover(pop, pop_size, num_bins)
			self.mutate(pop, num_bins)
			self.compute_bins(pop, num_bins)
			self.fitness_scores(pop, loc_alg, floor_alg, top_n)
		
		#Get the most fit bin size
		self.get_fittest(pop)
		
		
	def optimize_simple(self, loc_alg=2, floor_alg=1, top_n=3, num_guesses = 200):
		
			"""
			This function will optimize the bins for a certain
			set of test data.
			
			It randomly guesses the bin size and recomputes
			the error produced by the algorithm using this
			bin strategy.
			"""
			
			#Reset optimizer metadata
			cases = self.cases
			self.error = np.inf
			self.bins = None
			cases.reset()
			
			#Randomly guess bins
			for i in range(num_guesses):
			
				#r values are changes in rssi between the bins
				r2 = random.randint(-70, -10)
				r3 = random.randint(-70, -10)
				r4 = random.randint(-70, -10)
				
				#d values are changes in distance between the bins
				d1 = random.randint(1, 10)
				d2 = random.randint(1, 10)
				d3 = random.randint(1, 10)
				d4 = random.randint(1, 10)
			
				#This guesses the bin
				bins = [
					(r2 + r3 + r4, d1+d2+d3+d4),
					(r2 + r3, d1+d2+d3),
					(r2, d1+d2),
					(0, d1)
				]
				
				#Test the algorithm with this new strategy
				cases.reset()
				cases.test_algorithm(loc_alg=loc_alg, floor_alg=floor_alg, bin_strategy=(0, bins), top_n=top_n)
				if cases.net_xy_error < self.error:
					self.bins = bins
					self.error = cases.net_xy_error
				
				sys.stdout.write(str((i+1)/num_guesses) + "\r")
			
			
	def __str__(self):

		string = ""
		string += "Total Error: " + str(self.error) + "\n"
		string += "Bin Strategy: " + str(self.bins) + "\n"
		return string
	
