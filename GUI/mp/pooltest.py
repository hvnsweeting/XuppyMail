from multiprocessing import Pool

def f(x):
	return x*x

if __name__ == '__main__':
	po = Pool(processes=4)
	result = po.apply_async(f, [10])
	print result.get(timeout=1)
	print po.map(f, range(10))
