import numpy as np
import matplotlib.pyplot as plt

class Klant:
	def __init__(self, desc=-1, t_nodig=-1):
		self.desc=desc
		if self.desc==-1: self.desc=np.random.choice([0, 1], p=[1.0/3.0, 2.0/3.0])
		self.t_nodig=t_nodig
		if self.t_nodig==-1: self.t_nodig=\
		[
			np.random.choice([0.1, 0.3], p=[0.5, 0.5]),
			np.random.choice([0.2, 0.4], p=[0.5, 0.5])
		][self.desc]
		self.t_gehad=0
		self.rang=self.bepaal_rang()
	
	def bepaal_rang(self):
		return self.desc

def wachttijd():
	dt=0.01
	t_eind=2000
	n_t=int(t_eind/dt)
	rij=[]
	p_nieuw=0.003
	
	beurttijd=False
	
	desc_bediend=-1
	vertraagd=0
	
	k_spec=None
	t_spec_in=100
	
	for i in range(0, n_t):
		t=i*dt
		
		# Met kans p_nieuw een nieuwe klant in de rij
		if np.random.rand()<p_nieuw:
			k_nieuw=Klant()
			rij.append(k_nieuw)
		
		# Speciale klant
		if t==t_spec_in:
			k_spec=Klant()
			rij.append(k_spec)
		
		if vertraagd>0:
			# Afwezig, want vertraagd
			vertraagd-=dt
		elif len(rij)>0:
			# Vind kleinste klant (dit wordt k_min)
			rang_min=np.inf
			k_min=None
			for k in rij:
				if k.rang<rang_min:
					rang_min=k.rang
					k_min=k
			if desc_bediend==1 and k_min.desc==0 and len(rij)>1:
				# Voordringen levert vertraging op
				vertraagd=np.random.choice([0.1, 0.5], p=[0.5, 0.5])
			else:
				# Behandeling
				k_min.t_gehad+=dt
				if beurttijd and k_min is k_spec: return t-t_spec_in
				if k_min.t_gehad>=k_min.t_nodig:
					if k_min is k_spec: return t-t_spec_in
					rij.remove(k_min)
				else: k_min.rang=k_min.bepaal_rang()
			desc_bediend=k_min.desc

def main():
	n=10000
	tijden=np.empty(n)
	try:
		for i in range(n):
			print("i={}    \r".format(i), end="")
			tijden[i]=wachttijd()
		tijd_gem=np.mean(tijden)
	except KeyboardInterrupt:
		tijd_gem=np.mean(tijden[:i])
	print("\nGemiddelde wachttijd: {:.4f}".format(tijd_gem))

if __name__ == "__main__": main()