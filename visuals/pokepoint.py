from matplotlib.patches import Wedge, Circle
import matplotlib.pyplot as plt
from copy import copy
import numpy as np
from pathlib import Path
import sys

## we can add $PARENT_PATH to root, so we can run & import stuff inside
REPO_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_PATH))

from config.pokemon_config import TYPE_COLORS, STATUS_COLORS, STATUS_DMG

VERBOSE = True
CONFIG_PLOT_LASTLINE = False
_DEFAULT_RING_WIDTH = 0.075
_THIN_LINE_WIDTH = 0.5
_THICK_LINE_WIDTH = 1

def get_hpp_color(hpp_value):
    if hpp_value <= 0.25:
        hp_ring_color = 'red'
    elif hpp_value <= 0.5:
        hp_ring_color = 'yellow'
    else:
        hp_ring_color = 'green'
    return hp_ring_color

def notify(string):
    if not VERBOSE:
        return
    print(string)

class Pokepoint:
    def __init__(self, types, size=1.0, hp_pct=1.0, status=None):
        self.types = types if len(types)==2 else types*2
        self.size = size
        self.radius = 0.5 * self.size
        self.hp_pct = max(0, min(hp_pct, 1.0))  # Clamp to 0–1
        self.hpp_last = None
        self.total_status_dmg = 0
        self.status = status

    def set_status(self, status):
        self.status = status

    def reset_status(self):
        self.status = None

    def add_status_dmg(self, toxic_turn=1):
        current_dmg = STATUS_DMG.get(self.status, 0) * toxic_turn
        self.decrease_hp(current_dmg)
        self.total_status_dmg += current_dmg
        notify(f"Applied status damage: ({self.status} +{current_dmg}/{self.total_status_dmg}) =>  (HP: {self.hpp_last} -> {self.hp_pct})")

    def set_health(self, hp_pct):
        self.hpp_last = copy(self.hp_pct)
        self.hp_pct = max(0, min(hp_pct, 1.0))
        notify(f"Set health: {self.hpp_last} -> {self.hp_pct}")

    def reset_health(self):
        notify(f"Resetting health: Last/Current => {self.hpp_last}/{self.hp_pct} -> {None}/{1.0}")
        self.hpp_last = None # copy(self.hp_pct)
        self.hp_pct = 1.0

    def increase_hp(self, amount):
        if amount>1:
            amount = float(min(amount,100))/100 ## if this is greater than 1, assume it's a PERCENTAGE
        self.hpp_last = copy(self.hp_pct)
        self.hp_pct += amount
        notify("Increased health: {self.hpp_last} -> {self.hp_pct}")        

    def decrease_hp(self, amount):
        if amount>1:
            amount = float(min(amount,100))/100 ## if this is greater than 1, assume it's a PERCENTAGE
        self.hpp_last = copy(self.hp_pct)
        self.hp_pct -= amount
        notify(f"Decreased health: {self.hpp_last} -> {self.hp_pct}")        

    def convert_to_radius(self, hpp_value):
        return np.sqrt(hpp_value) * self.radius

    def draw(self, ax, x, y):
        ## we can IMMEDIATELY calculate all of the layers' radii: 
        #### (opt .status) radius_stat_ring, (main) self.radius, (after status dmg) non_status_dmg -> radius_between_atk_stat, (final health after atk) radius_for_inner
        radius_stat_ring = self.radius + _DEFAULT_RING_WIDTH 
        non_status_dmg = 1 - self.total_status_dmg
        radius_between_atk_stat = self.convert_to_radius(non_status_dmg) 
        radius_for_inner = self.convert_to_radius(self.hp_pct)

        # --- Draw status ring if needed ---
        if self.status in STATUS_COLORS:
            ring = Circle((x, y), 
                radius=radius_stat_ring, 
                facecolor=STATUS_COLORS[self.status],
                edgecolor='none', linewidth=0, 
                zorder=1)
            ax.add_patch(ring)
            notify(f"Added status ring: {self.status}")

        # --- Draw main 4-quadrant pokepoint ---
        angles = [(0, 90), (90, 180), (180, 270), (270, 360)]
        for i, (theta1, theta2) in enumerate(angles):
            color = TYPE_COLORS.get(self.types[i % 2], "#888888")
            wedge = Wedge(center=(x, y), 
                r=self.radius, theta1=theta1, theta2=theta2,
                facecolor=color, 
                edgecolor='none', linewidth=0, 
                zorder=2)
            ax.add_patch(wedge)
            notify(f"Added Pokepoint wedge: {self.types}@[{theta1},{theta2}] = {color}")

        # --- ADDING LAYER: Status DAMAGE
        if self.status and self.total_status_dmg>0:
            ## apply "ring" - which is a low-alpha circle, with high-alpha circles inside
            stat_ring_color = STATUS_COLORS[self.status]
            status_dmg_ring = Circle((x, y), 
                radius=self.radius, 
                facecolor=stat_ring_color, 
                alpha=0.5, 
                edgecolor=stat_ring_color, linestyle='dashed', linewidth=_THIN_LINE_WIDTH,
                zorder=3)
            ax.add_patch(status_dmg_ring)
            notify(f"Added status dmg: {self.status}: {self.radius} -> {radius_between_atk_stat}")

        # --- Draw delta-hp SHRINKING circle (if not full health) ---
        if non_status_dmg!=self.hp_pct:
            damaged_hpp = non_status_dmg - self.hp_pct ## this is the grey portion, not actually used because we already have our final hpp
            attack_dmg_ring = Circle((x, y), 
                radius=radius_between_atk_stat, 
                facecolor='#888888', 
                alpha=0.8, 
                edgecolor=stat_ring_color, linestyle='dashed', linewidth=_THIN_LINE_WIDTH, 
                zorder=4)
            ax.add_patch(attack_dmg_ring)
            notify(f"Added attack dmg: {radius_between_atk_stat} -> {radius_for_inner} <<< ???")

        ## finally, we can draw the health circle (inner circle), using the same 4-quad technique!
        for i, (theta1, theta2) in enumerate(angles):
            color = TYPE_COLORS.get(self.types[i % 2], "#888888")
            wedge = Wedge(center=(x, y), 
                r=radius_for_inner, theta1=theta1, theta2=theta2, 
                facecolor=color, alpha=1,
                edgecolor='none', linewidth=0,
                zorder=5)
            ax.add_patch(wedge)
            notify(f"Added Center Pokepoint wedge: {self.types}@[{theta1},{theta2}] = {color} @ r={radius_for_inner}")

        ## we'll wrap these wedges with an inner circle
        inner_line = Circle((x, y), 
            radius=radius_for_inner, 
            facecolor='none', 
            edgecolor=get_hpp_color(self.hp_pct), linewidth=_THICK_LINE_WIDTH, 
            zorder=6)
        ax.add_patch(inner_line)

        ## lastly, we can plot the last hpp
        if self.hpp_last and CONFIG_PLOT_LASTLINE:
            radius_for_last = self.convert_to_radius(self.hpp_last)
            last_hpp_color = get_hpp_color(self.hpp_last)
            last_line = Circle((x, y), 
                radius=radius_for_last, 
                facecolor='none', 
                # edgecolor=last_hpp_color, 
                edgecolor='#888888', linestyle='dashed', linewidth=_THIN_LINE_WIDTH,
                zorder=6)
            ax.add_patch(last_line)




