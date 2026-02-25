# src/build_master.py
from src.lca_io import load_material
import pandas as pd
from pathlib import Path

# Ensure output folder exists
Path("data/processed").mkdir(parents=True, exist_ok=True)

abs_df = load_material("ABS")
pp_df  = load_material("PP")
pla_df = load_material("PLA")

master = pd.concat([abs_df, pp_df, pla_df], ignore_index=True)
master.to_csv("data/processed/master_impacts.csv", index=False)

print("✅ Master impact table created: data/processed/master_impacts.csv")