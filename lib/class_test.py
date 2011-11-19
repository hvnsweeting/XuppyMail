#Create a class its method
class Simple1:
	#Every class must has __init__ function
	def __init__(self, name):
		self.name = name
	
	#Every method must has at least 1 arg :self . If it has more than 1, self must be the first
	def hello(self):
		print self.name + " says hi."

#Simple2 extends Simple1
class Simple2(Simple1):
	def goodbye(self):
		print self.name + " says bye."

me = Simple2("HVN")
me.hello()
me.goodbye()
