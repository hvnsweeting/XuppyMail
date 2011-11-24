from multiprocessing import Process, Queue
import os

def f(q):
	info('q process')
	q.put([42, None, 'Hello'])

def info(title):
	print title
	print 'parent process', os.getppid()
	print 'process id', os.getpid()

if __name__ == '__main__':
	info('main')
	q = Queue()
	p = Process(target=f, args=(q,))
	p.start()
	print q.get()
	p.join()
	
