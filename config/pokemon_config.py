## Some general config settings for Pokemon

TYPE_COLORS = {
    "Normal": "#A8A77A",
    "Fire": "#EE8130",
    "Water": "#6390F0",
    "Electric": "#F7D02C",
    "Grass": "#7AC74C",
    "Ice": "#96D9D6",
    "Fighting": "#C22E28",
    "Poison": "#A33EA1",
    "Ground": "#E2BF65",
    "Flying": "#A98FF3",
    "Psychic": "#F95587",
    "Bug": "#A6B91A",
    "Rock": "#B6A136",
    "Ghost": "#735797",
    "Dragon": "#6F35FC",
    "Dark": "#705746",
    "Steel": "#B7B7CE",
    "Fairy": "#D685AD",
}

STATUS_COLORS = {
    "PAR": "#FFD700",  # Yellow
    "BRN": "#A52A2A",  # Brown
    "FRZ": "#00BFFF",  # Light blue
    "SLP": "#9370DB",  # Purple
    "PSN": "#8B008B",  # Dark magenta
    "TOX": "#4B0082",  # Indigo
}

DEFAULT_TYPE_ORDER = [
    "Normal", "Fighting", "Flying",
    "Poison", "Ground", "Rock",
    "Bug", "Ghost", "Steel",
    "Fire", "Water", "Grass", "Electric", "Ice",
    "Psychic", "Dark", "Fairy",
    "Dragon"
]

STAT_NAME = {
    "hp": "HP",
    "atk": "Attack",
    "def": "Defense",
    "spa": "Sp. Atk",
    "spd": "Sp. Def",
    "spe": "Speed"
}
STAT_ABBR = {v:k for k,v in STAT_NAME.items()}

DEFAULT_STAT_ORDER = ['hp','atk','def','spa','spd','spe']

CATEGORY_ABBR = {
    "Physical": "Phys",
    "Special": "Spec",
    "Status": "Stat"
}
CATEGORY_NAME = {v:k for k,v in CATEGORY_ABBR.items()}

## some extra colors
COLOR_PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c",
    "#d62728", "#9467bd", "#8c564b",
    "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

FORME_TAGS_TO_IGNORE = [
    # "Gmax",       # Gigantamax
    # "Mega",       # Mega evolutions
    "Starter",    # Hisuian starters (maybe include?)
    "Cosmetic",   # e.g. Unown-A, Unown-B
    "Therian",    # Often same stats, diff model
    # "Totem",      # Totem Pokémon from USUM
    "Ash",        # Ash-Greninja etc.
    "Origin",     # Giratina-Origin
    "Alola",     # Uncomment to exclude regional forms
    "Galar",     #
    "Hisuian",   #
    "Paldea",    #
]


