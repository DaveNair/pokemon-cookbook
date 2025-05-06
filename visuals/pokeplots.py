_QUARTILE_VALUES = [25, 50, 75]
_OUTLIER_IQR_COFACTOR = 1.5 

class PokeHist():
	'''Historgram math is simple enough - this will be specialized to the Pokemon Cookbook.'''
	def __init__(self, values, labels=[], types=[]):
		## collect all the incomining values
		combined = [{'value':i} for i in values]
		for i in range(len(labels)):
			combined[i]['label'] = labels[i]
		for i in range(len(types)):
			combined[i]['types'] = types[i]

		## set histogram data
		self.data = sorted(combined, key = lambda entry: entry['value'])
		self.set_attrs()

	def set_attrs(self):
		combined = self.data
		self.elements = [combined[i]['value'] for i in range(len(combined))]
		self.labels = [combined[i].get('label', '') for i in range(len(combined))]
		self.types = [combined[i].get('types', (None, None)) for i in range(len(combined))]
		
		## now calculate metrics
		self.q1 = np.percentile(self.elements, _QUARTILE_VALUES[0])
		self.mu = np.mean(self.elements)
		self.median = np.percentile(self.elements, _QUARTILE_VALUES[0])
		self.q3 = np.percentile(self.elements, _QUARTILE_VALUES[0])
		self.IQR = Q3 - Q1
		self.lower_bound = Q1 - (IQR * _OUTLIER_IQR_COFACTOR)
		self.upper_bound = Q3 + (IQR * _OUTLIER_IQR_COFACTOR)

		## sigma? + left-normal? right-normal?
		self.sigma = np.std(self.elements)
		self.lsigma = np.std([i for i in self.elements if i<=self.median] + [self.median+(self.median-i) for i in self.elements if i<self.median])
		self.rsigma = np.std([i for i in self.elements if i>=self.median] + [self.median+(self.median-i) for i in self.elements if i>self.median])

		## outliers, including labels & types
		self.outliers = [entry for entry in self.data if self.lower_bound>=entry['value'] or self.upper_bound<=entry['value']]

	def keep(self, pkTypes):
		if type(pkTypes)!=list:
			pkTypes = [pkTypes]
		keep_indices = []
		old_N = len(self.data)
		for i in range(old_N):
			entry = self.data[i]
			if any([pkT in entry['types'] for pkT in pkTypes]):
				keep_indices.append(i)
		self.data = [self.data[i] for i in keep_indices]
		self.set_attrs()
		print(f"Kept {len(self.data)} out of {old_N} records.")

	def remove(self, pkTypes):
		if type(pkTypes)!=list:
			pkTypes = [pkTypes]
		keep_indices = []
		old_N = len(self.data)
		for i in range(old_N):
			entry = self.data[i]
			if any([pkT in entry['types'] for pkT in pkTypes]):
				continue
			keep_indices.append(i)
		self.data = [self.data[i] for i in keep_indices]
		self.set_attrs()
		print(f"Removed {old_N - len(self.data)} out of {old_N} records.")

