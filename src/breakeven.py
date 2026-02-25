# src/breakeven.py

from __future__ import annotations

from pathlib import Path
import math
import pandas as pd

from src.lca_io import load_material


def break_even_lifetime(abs_value: float, pla_base_value: float, reference_lifetime: float = 15.0) -> float:
    """
    Solve for L_PLA where:
        pla_base_value * (reference_lifetime / L_PLA) = abs_value
    =>  L_PLA = (pla_base_value * reference_lifetime) / abs_value

    Notes (important for LCA):
    - abs_value or pla_base_value can be negative (credits). That is allowed.
    - If abs_value == 0, the equation is undefined -> treated as +/- infinity depending on pla_base_value.
    """
    if abs_value == 0:
        # ABS has zero impact in this category; break-even undefined
        return math.inf
    return (pla_base_value * reference_lifetime) / abs_value


def classify_case(abs_value: float, pla_value: float, be: float, reference_lifetime: float) -> str:
    """
    Adds interpretation so results make sense for negative/zero values.
    """
    if abs_value == 0:
        return "ABS_zero_impact_break_even_undefined"

    if not math.isfinite(be):
        return "break_even_undefined"

    # If break-even lifetime <= 0, PLA is already better/worse in a non-physical way for lifetime scaling
    if be <= 0:
        # This happens when abs and pla have opposite signs (one is credit, one is burden)
        return "sign_mismatch_or_credit_case"

    if be <= reference_lifetime:
        return "feasible_within_reference"
    return "not_feasible_within_reference"


def compute_break_even_table(reference_lifetime: float = 15.0) -> pd.DataFrame:
    abs_df = load_material("ABS")
    pla_df = load_material("PLA")

    rows: list[dict] = []

    for cat in abs_df["impact_category"].unique():
        abs_val = float(abs_df.loc[abs_df["impact_category"] == cat, "value"].values[0])
        pla_val = float(pla_df.loc[pla_df["impact_category"] == cat, "value"].values[0])

        be = break_even_lifetime(abs_value=abs_val, pla_base_value=pla_val, reference_lifetime=reference_lifetime)

        feasible = (be > 0 and be <= reference_lifetime) if math.isfinite(be) else False
        status = classify_case(abs_val, pla_val, be, reference_lifetime)

        rows.append(
            {
                "impact_category": cat,
                "ABS_value": abs_val,
                "PLA_value": pla_val,
                "PLA_break_even_lifetime_years": (round(be, 2) if (math.isfinite(be) and be > 0) else float("nan")),
                "Feasible_within_reference_lifetime": feasible,
                "reference_lifetime_years": reference_lifetime,
                "status": status,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    reference_lifetime = 15.0

    Path("data/processed").mkdir(parents=True, exist_ok=True)

    result = compute_break_even_table(reference_lifetime=reference_lifetime)
    out_path = "data/processed/PLA_break_even_vs_ABS.csv"
    result.to_csv(out_path, index=False)

    print(f"✅ Break-even lifetime table created: {out_path}")
    print(result.head(10))


if __name__ == "__main__":
    main()