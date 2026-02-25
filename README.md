# openlca-results-analyzer

Python pipeline to parse openLCA Excel exports and reproduce durability scaling (DM) + PLA lifetime sensitivity (6/10/15 years). Generates clean tables ready for thesis and job portfolio.

## What it does
- Reads openLCA Excel exports (ABS / PP / PLA)
- Normalizes impact results into a master table
- Applies Durability Multiplier (DM = 15 / L_PLA)
- Exports reproducible sensitivity outputs (L_PLA = 6, 10, 15)

## Inputs
Place these files in `data/raw/`:
- Door_panel___ABS__foreground_.xlsx
- Door_panel___PP__foreground_.xlsx
- Door_panel___PLA__foreground_.xlsx

## How to run
```bash
pip install pandas openpyxl matplotlib jinja2
python -m src.build_master
python -m src.reproduce_dm