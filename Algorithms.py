
import lmfit, math, numpy as np
from collections import Counter

def loc_model1(params, x, y, prox):
    x0 = params['x0']
    y0 = params['y0']
    t = (x - x0)**2 + (y - y0)**2
    t = (t - prox)/prox
	
    return t

	
def loc_model2(params, x, y, prox):

    x0 = params['x0']
    y0 = params['y0']
    t = np.sqrt((x - x0)**2 + (y - y0)**2)
    t = (prox - t)/prox**2
	
    return t

	
def loc_model3(params, x, y, prox):
    x0 = params['x0']
    y0 = params['y0']
    t = np.sqrt((x - x0)**2 + (y - y0)**2)
    t = t/prox**2
	
    return t

	
def loc_model4(params, x, y, prox):
    x0 = params['x0']
    y0 = params['y0']
    t = (x - x0)**2 + (y - y0)**2
    t = t/prox**2
	
    return t
	
	
def find_floor_simple(floor, building_id):
    # making a list of tuples (floor, building_id)
    zipped = list(zip(floor, building_id))
    
    # counter object that has key(tuple) and value(count)
    c = Counter(x for x in zipped)
    
    # getting the 1 most common keys, gets a list of tuples(key, count) return the first tuple's key   
    return c.most_common(1)[0][0]


loc_algorithms = [
	0,
	loc_model1,
	loc_model2,
	loc_model3,
	loc_model4
]

floor_algorithms = [
	0,
	find_floor_simple
]

bin_strategies = [
	0,
	[(-70, 15), (-60, 7), (-50, 3), (0, 2)],
	[(-70, 9), (-60, 5), (-50, 2), (0, 1)],
	[(-143, 12), (-83, 9), (-51, 3), (0, 1)],
	[(-153, 11), (-84, 6), (-70, 2), (0, 1)]
]


