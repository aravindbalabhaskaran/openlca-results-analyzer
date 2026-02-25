# src/lca_io.py
import pandas as pd
from pathlib import Path

def load_openlca_impacts(filepath: str | Path) -> pd.DataFrame:
    """
    Reads openLCA Excel export (sheet: 'Impacts') and returns clean table:
    impact_category, unit, value
    """
    df = pd.read_excel(filepath, sheet_name="Impacts")

    # openLCA exports often have metadata rows; keep rows where key columns exist
    df = df.dropna(subset=["Unnamed: 2", "Unnamed: 4"])

    clean = pd.DataFrame({
        "impact_category": df["Unnamed: 2"].astype(str).str.strip(),
        "unit": df["Unnamed: 3"].astype(str).str.strip(),
        "value": pd.to_numeric(df["Unnamed: 4"], errors="coerce"),
    }).dropna(subset=["value"])

    return clean.reset_index(drop=True)

def load_material(material: str, base_path: str = "data/raw") -> pd.DataFrame:
    """
    material: 'ABS', 'PP', or 'PLA'
    Loads corresponding openLCA export from data/raw and adds 'material' column.
    """
    file_map = {
        "ABS": "Door_panel___ABS__foreground_.xlsx",
        "PP": "Door_panel___PP__foreground_.xlsx",
        "PLA": "Door_panel___PLA__foreground_.xlsx",
    }

    material = material.upper().strip()
    if material not in file_map:
        raise ValueError(f"Unknown material '{material}'. Use one of: {list(file_map)}")

    path = Path(base_path) / file_map[material]
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    out = load_openlca_impacts(path)
    out["material"] = material
    return out