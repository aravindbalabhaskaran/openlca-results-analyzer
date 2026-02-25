# src/reproduce_dm.py
from pathlib import Path
from src.lca_io import load_material
from src.metrics import durability_multiplier

# Ensure output folder exists
Path("data/processed").mkdir(parents=True, exist_ok=True)

L_ABS = 15.0  # reference petro lifetime in years

pla = load_material("PLA")

for l_pla in (6.0, 10.0, 15.0):
    dm = durability_multiplier(L_ABS, l_pla)

    df = pla.copy()
    df["L_PLA"] = l_pla
    df["DM"] = dm
    df["value"] = df["value"] * dm

    out = f"data/processed/PLA_DML{int(l_pla)}.csv"
    df.to_csv(out, index=False)
    print(f"✅ Wrote {out}")

print("✅ PLA sensitivity reproduced (DM scaling)")