# src/breakeven.py

def break_even_lifetime(abs_value, pla_base_value, reference_lifetime=15):
    """
    Solve for L_PLA where:
    pla_base * (reference_lifetime / L_PLA) = abs_value

    => L_PLA = (pla_base * reference_lifetime) / abs_value
    """
    if abs_value <= 0:
        raise ValueError("abs_value must be > 0")
    if pla_base_value < 0:
        raise ValueError("pla_base_value must be >= 0")
    return (pla_base_value * reference_lifetime) / abs_value


if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path
    from src.lca_io import load_material

    reference_lifetime = 15

    abs_df = load_material("ABS")
    pla_df = load_material("PLA")

    rows = []
    for cat in abs_df["impact_category"].unique():
        abs_val = abs_df.loc[abs_df["impact_category"] == cat, "value"].values[0]
        pla_val = pla_df.loc[pla_df["impact_category"] == cat, "value"].values[0]

        be_lifetime = break_even_lifetime(
            abs_value=abs_val,
            pla_base_value=pla_val,
            reference_lifetime=reference_lifetime
        )

        feasible = be_lifetime <= reference_lifetime

        rows.append({
            "impact_category": cat,
            "PLA_break_even_lifetime_years": round(be_lifetime, 2),
            "Feasible_within_15_years": feasible
        })

    result = pd.DataFrame(rows)

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    out_path = "data/processed/PLA_break_even_vs_ABS.csv"
    result.to_csv(out_path, index=False)

    print(f"✅ Break-even lifetime table created: {out_path}")