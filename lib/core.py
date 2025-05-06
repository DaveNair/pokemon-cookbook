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
