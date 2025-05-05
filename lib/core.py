## Core file for pkmn-cookbook
## by Dave Nair
import json
from pathlib import Path
import sys
import numpy as np

# --- I/O ---

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

POKEDEX_PATH = ROOT / Path("data/processed/pokedex.json")

def load_pokedex():
	with open(POKEDEX_PATH, "r", encoding="utf-8") as f:
		return json.load(f)

POKEDEX = load_pokedex()

def get_pokedata(pkname, dexkey):
	try:
		return POKEDEX.get(
			pkname.strip().lower(), 
			{dexkey: None}
			).get(dexkey, None)
	except Exception as e:
		print(f"[{e}] Could not retrieve {pkname.strip().lower()}.{dexkey} from POKEDEX.")
		sys.exit(1)
	return None

# --- Math ---

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
		self.elements = [combined[i]['value'] for i in range(len(combined))]
		self.labels = [combined[i].get('label', '') for i in range(len(combined))]
		self.types = [combined[i].get('types', (None, None)) for i in range(len(combined))]

	def get_values(self):
		return [combined[i]['value'] for i in range(len(combined))]

	def get_labels(self):
		return [combined[i].get('label', '') for i in range(len(combined))]

	def get_types(self):
		return [combined[i].get('types', (None, None)) for i in range(len(combined))]

	def calculate_metrics(self):
		## each of these are np.float64 scalar values 
		self.q1 = np.percentile(self.elements, _QUARTILE_VALUES[0])
		self.mean = np.mean(self.elements)
		self.median = np.percentile(self.elements, _QUARTILE_VALUES[0])
		self.q3 = np.percentile(self.elements, _QUARTILE_VALUES[0])
		self.IQR = Q3 - Q1
		self.lower_bound = Q1 - (IQR * _OUTLIER_IQR_COFACTOR)
		self.upper_bound = Q3 + (IQR * _OUTLIER_IQR_COFACTOR)

		## mu? sigma?
		## left-normal? right-normal?

		## outliers, including labels & types

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
		print(f"Removed {old_N - len(self.data)} out of {old_N} records.")

	def plot(self):
		return 

