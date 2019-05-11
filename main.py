
from TestData import *
from TestAlgorithm import *
from Visualize import *
from OptimizeBins import *

def main_test_sim():
	
	#Open the test cases for a certain building
	print("Opening test cases")
	cases = TestCases(out="sim_results.csv")
	cases.open_test_data(path="SimulatedData.csv", building="SB")
	
	#Run the original bins over the new test data
	print("Testing original bin strategy")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 2)
	cases.to_csv()
	
	#Run the new bins over the new test data
	print("Testing new bin strategy")
	cases.test_algorithm(loc_alg = 2, floor_alg = 1, bin_strategy = 3)
	cases.to_csv()


def main_optimize_bins():

	#Open the test cases for a certain building
	print("Opening test cases")
	bins = BinOptimizer()
	bins.open_test_data(path="Datasets/database.csv", building="SB", interval=5, sample=100)
	
	#Simple optimization
	print("Optimizing Bins - Simple")
	bins.optimize(loc_alg=loc_algorithms[2], floor_alg=floor_algorithms[1], top_n=3, pop_size = 5000, num_generations=0)
	print(bins)
		
	#Genetic optimization
	print("Optimizing Bins - Genetic")
	bins.optimize(loc_alg=loc_algorithms[2], floor_alg=floor_algorithms[1], top_n=3, pop_size = 50, num_generations=100)
	print(bins)
	
	exit()
	
	

	#Open the test cases for a certain building
	print("Opening test cases")
	bins.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	
	#Run the new bins over the new test data
	print("Optimizing Bins")
	bins.optimize(loc_alg=loc_algorithms[2], floor_alg=floor_algorithms[1], top_n=3, pop_size = 50, num_generations=5)
	print(bins)
	

def main_visualize():
	df = load_results("Datasets//results_SB_5s_2.csv")
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=2, save_path="./SB01_5s_2.html", interval=5, results=(0, 100))
	
	df = load_results("Datasets//results_SB_5s_6.csv")
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=6, save_path="./SB01_5s_6.html", interval=5, results=(0, 100))
	
	df = load_results("Datasets//results_SB_10s_6.csv")
	view_tests(df, building="SB", loc_alg=2, floor=1, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=6, save_path="./SB01_10s_6.html", interval=10, results=(0, 100))
	
	
	
	
	df = load_results("Datasets//results_SB_5s_2.csv")
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=2, save_path="./SB02_5s_2.html", interval=5, results=(0, 100))
	
	df = load_results("Datasets//results_SB_5s_6.csv")
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=6, save_path="./SB02_5s_6.html", interval=5, results=(0, 100))
	
	df = load_results("Datasets//results_SB_10s_6.csv")
	view_tests(df, building="SB", loc_alg=2, floor=2, days=[(2019, 2, 1), (2019, 3, 29)], bin_strategy=6, save_path="./SB02_10s_6.html", interval=10, results=(0, 100))
	

def main_test_alg():

	#Open the test cases for a certain building (5sec)
	print("Opening test cases")
	cases = TestCases(out="Datasets/results_SB_5s_2.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[2])
	cases.to_csv()
	print(cases.net_xy_error)
	
	
	#Open the test cases for a certain building (5sec)
	print("Opening test cases")
	cases = TestCases(out="Datasets/results_SB_5s_6.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[6])
	cases.to_csv()
	print(cases.net_xy_error)
	
	
	#Open the test cases for a certain building (10sec)
	print("Opening test cases")
	cases = TestCases(out="Datasets/results_SB_10s_7.csv")
	cases.open_test_data(path="Datasets/database.csv", building="SB", interval=10)
	cases.test_algorithm(loc_alg = loc_algorithms[2], floor_alg = floor_algorithms[1], bin_strategy = bin_strategies[7])
	cases.to_csv()
	print(cases.net_xy_error)


def main():
	main_optimize_bins()
	#main_test_alg()
	#main_visualize()

if __name__ == "__main__":
	main()

	
	
	