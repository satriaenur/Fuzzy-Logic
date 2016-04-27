from random import *
from math import *
from fuzzy import *

with open("data_training.csv", "r") as ins:
	data_training = []
	for line in ins:
		a = (line.replace("\n","").replace("_","").lower()).split(',')
		a[0] = float(a[0])
		a[1] = float(a[1])
		a[2] = float(a[2])
		a[3] = int(a[3])
		data_training.append(a)

class kromosom:
	def __init__(self, nilai):
		self.nilai = nilai
		self.fitness = 0
		self.setfitness()

	def setfitness(self):
		fuzz = fuzzy(data_training,self.nilai)
		self.fitness = fuzz.akurasi + 1

class GA:
	def __init__(self, populasi,generasi):
		self.populasi = populasi
		self.jmlkromosom = 27
		self.jmlElitism = 2
		self.generasi = generasi
		self.individu = []
		self.parent = []
		self.elitism = []
		self.mutationrate = 1
		self.newindividu = []
		self.initial()

	def initial(self):
		for i in range(self.populasi):
			a = [randint(0,3) for j in xrange(self.jmlkromosom)]
			self.individu.append(kromosom(a))
		self.individu.sort(key=lambda x:x.fitness, reverse=True)
		for i in xrange(self.jmlElitism):
			self.elitism.append(self.individu[i])
		self.individu += self.elitism


	def parentselection(self):
		totalFitness = 0
		self.parent = []
		for i in self.individu:
			totalFitness = totalFitness + i.fitness
		while(len(self.parent)<self.populasi/2):
			bapakibu = []
			while True:
				dart = uniform(0,totalFitness)
				n = 0
				for k in self.individu:
					n = n + k.fitness
					if dart<=n:
						break
				if len(bapakibu)==0:
					bapakibu.append(k)
				else:
					if bapakibu[0].nilai != k.nilai:
						bapakibu.append(k)
						break
			self.parent.append(bapakibu)

	def recombination(self):
		awal = randint(1,self.jmlkromosom-2)
		akhir = randint(1,self.jmlkromosom-2)
		if(awal>akhir):
			awal,akhir = akhir,awal
		for i in self.parent:
			self.newindividu.append(kromosom(i[0].nilai[:awal]+i[1].nilai[awal:akhir]+i[0].nilai[akhir:]))
			self.newindividu.append(kromosom(i[1].nilai[:awal]+i[0].nilai[awal:akhir]+i[1].nilai[akhir:]))

	def mutation(self):
		for i in range(len(self.newindividu)):
			rate = random()
			if rate<=self.mutationrate:
				titik1 = randint(0,self.jmlkromosom-2)
				titik2 = randint(0,self.jmlkromosom-2)
				if titik1 == titik2: titik2 += 1
				self.newindividu[i].nilai[titik1] = randint(0,3)
				self.newindividu[i].nilai[titik2] = randint(0,3)
				self.newindividu[i] = kromosom(self.newindividu[i].nilai)

	def survivorselection(self):
		# skema mengganti semua generasi lama dengan generasi baru
		self.newindividu.sort(key=lambda x:x.fitness, reverse=True)
		for i in xrange(self.jmlElitism):
			if self.elitism[i].fitness < self.newindividu[i].fitness: self.elitism[i] = kromosom(self.newindividu[i].nilai)
		self.individu = self.newindividu[:self.populasi]+self.elitism

	def run(self):
		i = 0
		while(i < self.generasi):
			print "generasi ke-",i
			i+=1
			self.parentselection()
			self.recombination()
			self.mutation()
			self.survivorselection()
			# for ind in xrange(1,len(self.individu)):
			# 	if(self.individu[ind].nilai != self.individu[ind-1].nilai): break
			# if ind >= self.populasi/2:
			# 	for j in range(self.populasi/2):
			# 		randinit = randint(0,len(self.individu)-1-self.jmlElitism)
			# 		self.individu[randinit] = kromosom([randint(0,3) for x in xrange(self.jmlkromosom)])
			print self.elitism[0].nilai,":",self.elitism[0].fitness-1

class __main__:
	fuzzyGA = GA(35,1000)
	fuzzyGA.run()
