from itertools import *

data = [[1,2,3],[1,2,3]]

for x in product(*data):
	print x