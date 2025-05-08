import matplotlib.pyplot as plt

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

	def plot_boxes(self, fig=None, axs=None, ax_xy=None, ax=None, 
			orientation='vertical', symbols='', whiskers=(0.,1 0.9), 
			colors=None, xticks=None, title=None, ylabel=None, 
			boxprops=dict(linestyle='-', linewidth=1, color='black'), 
			flierprops=dict(marker='o', markersize=1, markeredgecolor='none'),
			meanprops=dict(linestyle='--')):
		## set fig & ax -> now expanded to multiple axs
		if ax is not None:
			target_ax = ax
			if fig is None:
				fig = ax.figure
		elif axs is not None and ax_xy is not None:
			target_ax = axs[ax_xy]
			if fig is None:
				fig = target_ax.figure
		else:
			fig, target_ax = plt.subplots()

		## add some quick things
		if ylabel:
			target_ax.set_ylabel(ylabel)

		## plot, including logic for multiple xticks
		if xticks is None:
			boxdata = self.data
		else:
			if type(xticks)==str and xticks.strip().lower() in ['type','types']:
				boxdata = self.partition_by_type()
			if type(xticks)==str and xticks.strip().lower() in ['gen']:
				boxdata = self.partition_by_gen()

		current_bplot = target_ax.boxplot(
			boxdata, orientation=orientation, sym=symbols, whis=whiskers, 
			patch_artist=True, tick_labels=xticks, 
			showcaps=False, showfliers=False, boxprops=boxprops, flierprops=flierprops, meanprops=meanprops, meanline=True)
		if title:
			target_ax.set_title(title)
		if colors:
			for patch, color in zip(current_bplot['boxes'], colors):
				patch.set_facecolor(color)

		return fig, target_ax

'''
import matplotlib.pyplot as plt
import numpy as np
from visuals.pokepoint import Pokepoint  # adjust as needed
from config.pokemon_config import TYPE_COLORS

# Example Inputs
BaseStatList = [25, 50, 65, 70, 71, 72, 73, 74, 75, 76, 77, 80, 120]  # example data
TypeList = [['Grass'], ['Grass'], ['Grass'], ['Grass'], ['Grass'], 
            ['Grass'], ['Grass'], ['Grass'], ['Grass'], ['Grass'], 
            ['Grass'], ['Grass'], ['Fire']]  # matching types

# Step 1: Compute outliers using IQR
sorted_stats = sorted(BaseStatList)
q1 = np.percentile(sorted_stats, 25)
q3 = np.percentile(sorted_stats, 75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

# Find outliers
outlier_indices = [i for i, val in enumerate(BaseStatList)
                   if val < lower_fence or val > upper_fence]

# Optional: define horizontal jitter function
def x_jitter_fn(index, base_x=1.0):
    # simple example: spread evenly around the x-position of boxplot
    return base_x + 0.05 * (index - len(outlier_indices) // 2)

# Step 2: Create plot
fig, ax = plt.subplots(figsize=(5, 6))

# Plot the base boxplot
ax.boxplot(BaseStatList, positions=[1])

# Step 3: Overlay Pokepoints for outliers
for count, i in enumerate(outlier_indices):
    val = BaseStatList[i]
    types = TypeList[i]
    pp = Pokepoint(types=types, size=0.2)  # You can adjust size here
    x = x_jitter_fn(count)  # Jittered x position
    pp.draw(ax=ax, center=(x, val))  # Draw Pokepoint

# Step 4: Cleanup and labels
ax.set_xticks([1])
ax.set_xticklabels(['Atk'])  # or whatever stat this is
ax.set_ylabel('Base Stat Value')
ax.set_title('Base Stat Distribution with Outliers as Pokepoints')

plt.show()
'''
