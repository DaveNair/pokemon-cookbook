from matplotlib.patches import Wedge, Circle
import matplotlib.pyplot as plt
from pathlib import Path
import sys

## we can add $PARENT_PATH to root, so we can run & import stuff inside
REPO_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_PATH))

from config.pokemon_config import TYPE_COLORS, STATUS_COLORS

class Pokepoint:
    def __init__(self, types, size=1.0, hp_pct=1.0, status=None):
        self.types = types if len(types)==2 else types*2
        self.size = size
        self.hp_pct = max(0, min(hp_pct, 1.0))  # Clamp to 0–1
        self.hpp_last = self.hp_pct
        self.total_burn_dmg = 0
        self.total_poison_dmg = 0
        self.total_toxic_dmg = 0
        self.status = status

    def set_status(self, status):
        self.status = status

    def reset_status(self):
        self.status = None

    def add_burn_dmg(self):
        current_burn_dmg = None
        self.decrease_hp(current_burn_dmg)
        self.total_burn_dmg += current_burn_dmg

    def add_poison_dmg(self):
        current_psn_dmg = None
        self.decrease_hp(current_psn_dmg)
        self.total_poison_dmg += current_psn_dmg

    def add_toxic_dmg(self, toxic_turn):
        ''' FINISH THIS'''
        current_toxic_dmg = toxic_turn / 16.0
        self.decrease_hp(current_toxic_dmg)
        self.total_toxic_dmg += current_toxic_dmg

    def set_health(self, hp_pct):
        self.hp_pct = max(0, min(hp_pct, 1.0))

    def reset_health(self):
        self.hp_pct = 1.0

    def increase_hp(self, amount):
        if amount>1:
            amount = float(min(amount,100))/100 ## if this is greater than 1, assume it's a PERCENTAGE
        self.hpp_last = self.hp_pct
        self.hp_pct += amount        

    def decrease_hp(self, amount):
        if amount>1:
            amount = float(min(amount,100))/100 ## if this is greater than 1, assume it's a PERCENTAGE
        self.hpp_last = self.hp_pct
        self.hp_pct -= amount        

    def draw(self, ax, x, y):
        base_r = 0.5 * self.size

        # --- Draw status ring if needed ---
        if self.status in STATUS_COLORS:
            ring = Circle((x, y), radius=base_r + 0.1, facecolor=STATUS_COLORS[self.status],
                          edgecolor='none', zorder=1)
            ax.add_patch(ring)

        # --- Draw main 4-quadrant pokepoint ---
        angles = [(0, 90), (90, 180), (180, 270), (270, 360)]
        for i, (theta1, theta2) in enumerate(angles):
            color = TYPE_COLORS.get(self.types[i % 2], "#888888")
            wedge = Wedge(center=(x, y), r=base_r, theta1=theta1, theta2=theta2,
                          facecolor=color, edgecolor='black', linewidth=0.5, zorder=2)
            ax.add_patch(wedge)

        # --- ADDING LAYER: Status DAMAGE

        # --- (technically adding a layer in below logic)

        # --- Draw delta-hp SHRINKING circle (if not full health) ---

        # --- Draw inner health hole (if not full health) --- <<< THIS IS GETTING REPLACED ABOVE & BELOW
        if self.hp_pct < 1.0:
            inner_r = base_r * (1.0 - self.hp_pct)
            if self.hp_pct <= 0.25:
                hp_ring_color = 'red'
            elif self.hp_pct <= 0.5:
                hp_ring_color = 'yellow'
            else:
                hp_ring_color = 'green'
            inner_circle = Circle((x,y), radius=inner_r, 
                facecolor='#888888', alpha=0.8, 
                # edgecolor=hp_ring_color, linewidth=0.25, 
                zorder=3)
            ax.add_patch(inner_circle)

            ## after adding the inner "ring", we will need to add an inner circle with normal colors - showing remaining hp


