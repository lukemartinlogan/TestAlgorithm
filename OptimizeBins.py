
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

class Bins:
	
	def __init__(self, num_bins):
	
		"""
		Keeps track of RSSI to distance
		mappings.
		"""
		
		self.num_bins = num_bins
		self.rssi = [0] + [random.randint(-70, -10) for i in range(self.num_bins-1)]
		self.dist = [random.randint(1, 10) for i in range(num_bins)]
		self.bins = []
		self.score = np.inf
	
	
	def compute_bins(self):
	
		"""
		This function will compute the bins
		using the bin widths.
		"""
		
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

		
	def initial_population(self, pop_size, num_bins):
		
		"""
		Randomly select a set of binning
		strategies and creates their
		initial scores.
		
		Bin strategies are considered
		"chromosomes".
		"""
		
		pop = []
		
		for i in range(pop_size):
			pop.append(Bins(num_bins))
		
		return pop
		
		
	def compute_bins(self, pop):
	
		"""
		This function will compute the bins
		using the bin widths.
		"""
		
		for bins in pop:
			bins.compute_bins()
		
	
	def fitness_scores(self, pop, loc_alg, floor_alg, top_n):
	
		"""
		Computes the fitness of each bin in the current
		population. Fitness is defined to be the total
		error in location estimates produced by this
		bin size.
		"""
		
		#Test the algorithm with this new strategy
		for i,bins in enumerate(pop):
			sys.stdout.write(str(i/len(pop)) + "        \r")
			sys.stdout.flush()
			self.cases.reset()
			bin_strategies[-1] = bins.bins
			self.cases.test_algorithm(loc_alg=loc_alg, floor_alg=floor_alg, bin_strategy=-1, top_n=top_n)
			bins.score = self.cases.net_xy_error
		print()
	
	
	def selection(self, pop):
	
		"""
		Selects a subset of the current population of
		chromosomes to evolve from. It will select either
		two genes or the top 20% of genes.
		"""
		
		#Sort population by fitness
		pop.sort(key = lambda bins : bins.score)
		
		#Select the top 20%
		if len(pop) * .2 >= 2:
			return pop[0:int(len(pop)*.2)]
				
		#Select the top two
		return pop[0:2]

	
	def crossover(self, pop, pop_size, num_bins):
	
		"""
		Combines different bins using the
		currently best bin strategies to
		form a new population.
		"""
		
		new_pop = pop.copy()
		
		for i in range(pop_size - len(pop)):
			
			#Select two random chromosomes
			bins1 = pop[random.randrange(0, len(pop))]
			bins2 = pop[random.randrange(0, len(pop))]
			bins = Bins(num_bins)
			
			#Merge the rssi bins
			for i in range(1, num_bins):
				
				#Generate probability
				prob = random.random()
				
				#Smaller
				if prob < 1/3:
					if bins1.rssi[i] <= -10/.75:
						bins.rssi[i] = bins1.rssi[i]*.75
				
				#Larger
				elif prob < 2/3:
					if bins2.rssi[i] >= -70/1.25:
						bins.rssi[i] = bins2.rssi[i]*1.25
				
				#Average
				else:
					bins.rssi[i] = (bins1.rssi[i] + bins2.rssi[i])/2
			
			#Merge the distance bins
			for i in range(num_bins):
				
				#Generate probability
				prob = random.random()
				
				#Smaller
				if prob < 1/3:
					if bins1.dist[i] >= 1/.75:
						bins.dist[i] = bins1.dist[i]*.75
				
				#Larger
				elif prob < 2/3:
					if bins2.dist[i] <= 10/1.25:
						bins.dist[i] = bins2.dist[i]*1.25
				
				#Average
				else:
					bins.dist[i] = (bins1.dist[i] + bins2.dist[i])/2
			
			#Add the new bin strategy to the population
			new_pop.append(bins)
		
		return new_pop
	
	
	def mutate(self, pop, num_bins):
		
		"""
		This function will randomly change
		some of the bins in the population.
		"""
		
		for bins in pop[2:]:
			
			#Replace some rssi bins
			prob = random.random()
			if prob < .2:
				for i in range(1, num_bins):
					prob = random.random()
					if prob < .2:
						bins.rssi[i] = random.randint(-70, -10)
			
			#Replace some distance bins
			prob = random.random()
			if prob < .2:
				for i in range(num_bins):
					prob = random.random()
					if prob < .2:
						bins.dist[i] = random.randint(1, 10)

		
	def get_fittest(self, pop):
		
		for bins in pop:
			if bins.score < self.error:
				self.error = bins.score
				self.bins = bins.bins
	
	
	def optimize(self, loc_alg, floor_alg, top_n=3, num_bins = 4, pop_size = 50, num_generations = 0):
	
		"""
		A genetic algorithm for finding the optimal bin
		sizes for a given set of test data. 
		
		loc_alg: A tuple of the following form: (id, loc_algorithm_model)
		floor_alg: A tuple of the following form: (id, floor_algorithm_model)
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
		self.compute_bins(pop)
		
		print("Generation " + str(0) + "/" + str(num_generations))
		self.fitness_scores(pop, loc_alg, floor_alg, top_n)
		print()
		
		#Evolve population
		prior_score = np.inf
		for i in range(num_generations-1):
			print("Generation " + str(i+1) + "/" + str(num_generations))
			pop = self.selection(pop)
			pop = self.crossover(pop, pop_size, num_bins)
			self.mutate(pop, num_bins)
			self.compute_bins(pop)
			self.fitness_scores(pop, loc_alg, floor_alg, top_n)
			print()
		
		#Get the most fit bin size
		self.get_fittest(pop)
	
	
	def __str__(self):

		string = ""
		string += "Total Error: " + str(self.error) + "\n"
		string += "Bin Strategy: " + str(self.bins) + "\n"
		return string
	
