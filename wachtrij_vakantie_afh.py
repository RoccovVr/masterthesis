import numpy as np
import matplotlib.pyplot as plt

class Klant:
	def __init__(self, desc=-1, t_nodig=-1):
		self.desc=desc
		if self.desc==-1: self.desc=np.random.choice([0, 1], p=[0.7, 0.3])
		self.t_nodig=t_nodig
		if self.t_nodig==-1: self.t_nodig=\
		[
			np.random.choice([0.2, 0.4], p=[0.25, 0.75]),
			np.random.choice([0.4, 0.6], p=[0.20, 0.80])
		][self.desc]
		self.t_gehad=0
		self.rang=self.bepaal_rang()
	
	def bepaal_rang(self):
		if self.desc==0:
			if self.t_gehad<0.1: return 1
			if self.t_gehad<0.2: return 3
			if self.t_gehad<0.3: return 1
			return 2
		if self.desc==1:
			if self.t_gehad<0.1: return 4
			if self.t_gehad<0.2: return 1
			if self.t_gehad<0.3: return 2
			return 3

def wachttijd():
	dt=0.01
	t_eind=2000
	n_t=int(t_eind/dt)
	rij=[]
	p_nieuw=0.005
	labda_vakantie=1
	
	beurttijd=False
	
	k_spec=None
	t_spec_in=100
	
	tijd_vakantie=-1
	met_vakantie=0
	
	for i in range(0, n_t):
		t=i*dt
		
		# Met kans p_nieuw een nieuwe klant in de rij
		if np.random.rand()<p_nieuw:
			k_nieuw=Klant()
			rij.append(k_nieuw)
		
		# Speciale klant
		if t==t_spec_in:
			k_spec=Klant(0, 2)
			rij.append(k_spec)
		
		if met_vakantie>0:
			# Afwezig, want met vakantie
			met_vakantie-=dt
		else:
			# Aanwezig
			if len(rij)==0:
				# Ga met vakantie voor willekeurige, exponentieel verdeelde tijd
				if tijd_vakantie==-1:
					tijd_vakantie=int(np.random.exponential(scale=1/labda_vakantie)/dt)*dt
				met_vakantie=tijd_vakantie
			else:
				# Vind kleinste klant (dit wordt k_min)
				rang_min=np.inf
				k_min=None
				for k in rij:
					if k.rang<rang_min:
						rang_min=k.rang
						k_min=k				
				# Behandeling
				k_min.t_gehad+=dt
				if beurttijd and k_min is k_spec: return t-t_spec_in
				if k_min.t_gehad>=k_min.t_nodig:
					if k_min is k_spec: return t-t_spec_in
					rij.remove(k_min)
				else: k_min.rang=k_min.bepaal_rang()

def main():
	n=5000
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