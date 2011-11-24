from multiprocessing import Process
import os

def info(title):
	print title
	print 'parent process', os.getppid()
	print 'process id', os.getpid()

def f(name):
	info('function f')
	print 'hello', name

if __name__ == '__main__':
	info('main')
	p = Process(target=f, args=('HVN',))
	p.start()
	p.join()

