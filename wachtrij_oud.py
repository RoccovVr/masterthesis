import numpy as np
import matplotlib.pyplot as plt

class Klant:
	def __init__(self, desc=-1, t_nodig=-1):
		# self.actief=False
		self.desc=desc
		if self.desc==-1: self.desc=np.random.choice([0, 1], p=[0.7, 0.3])
		# print("k {}".format(self.desc))
		self.t_nodig=t_nodig
		if self.t_nodig==-1: self.t_nodig=\
		[
			np.random.choice([1, 2], p=[0.25, 0.75]),
			np.random.choice([2, 3], p=[0.20, 0.80])
		][self.desc]
		self.t_gehad=0
		self.rang=self.bepaal_rang()
	
	def bepaal_rang(self):
		if self.desc==0:
			if self.t_gehad<0.5: return 1
			if self.t_gehad<1.0: return 3
			if self.t_gehad<1.5: return 1
			return 2
		if self.desc==1:
			if self.t_gehad<0.5: return 4
			if self.t_gehad<1.0: return 1
			if self.t_gehad<1.5: return 2
			return 3

def wachttijd():
	dt=0.01
	t_eind=2000
	n_t=int(t_eind/dt)
	rij=[]
	p_nieuw=0.005
	
	k_spec=None
	t_spec_in=100
	t_spec_uit=None
	t_spec_bed=None
	t_spec=None
	
	gesch=np.zeros(n_t)
	
	for i in range(0, n_t):
		t=i*dt
		
		# Met kans p_nieuw een nieuwe klant in de rij
		if np.random.rand()<p_nieuw:
			rij.append(Klant(0))
		
		# Speciale klant
		if t==t_spec_in:
			k_spec=Klant(0, 2)
			rij.append(k_spec)
		
		# Vind kleinste klant (dit wordt k_min)
		rang_min=np.inf
		k_min=None
		for k in rij:
			if k.rang<rang_min:
				rang_min=k.rang
				k_min=k
		
		# Behandeling
		if k_min is not None:
			k_min.t_gehad+=dt
			if k_min is k_spec and t_spec_bed is None:
				t_spec_bed=t
				t_spec=t_spec_bed-t_spec_in
				return t_spec
			if k_min.t_gehad>=k_min.t_nodig:
				if k_min is k_spec:
					t_spec_uit=t
					t_spec=t_spec_uit-t_spec_in					
					# break
					return t_spec
				rij.remove(k_min)
			else: k_min.rang=k_min.bepaal_rang()
	
		# print("Lengte rij: {}       \r".format(len(rij)), end="")
		# print("Lengte rij: {}".format(len(rij)))
		gesch[i]=len(rij)
		
	# print("Tijd speciale klant: {}".format(t_spec))
	# plt.plot(np.arange(n_t)*dt, gesch)
	# plt.show()
	# return t_spec

def main():
	n=10000
	tijden=np.empty(n)
	for i in range(n):
		try:
			print("i={}    \r".format(i), end="")
			tijden[i]=wachttijd()
		except KeyboardInterrupt: break
	print("\n")
	tijd_gem=np.mean(tijden[:i+1])
	print("Gemiddelde wachttijd: {:.4f}".format(tijd_gem))

if __name__ == "__main__": main()