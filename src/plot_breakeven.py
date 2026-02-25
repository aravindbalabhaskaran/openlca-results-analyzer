# src/plot_breakeven.py

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    in_path = Path("data/processed/PLA_break_even_vs_ABS.csv")
    if not in_path.exists():
        raise FileNotFoundError(
            "Missing break-even CSV. Run this first:\n"
            "  python -m src.breakeven"
        )

    df = pd.read_csv(in_path)

    # Keep only physically meaningful break-even lifetimes (positive + finite)
    df = df.dropna(subset=["PLA_break_even_lifetime_years"]).copy()
    df = df[df["PLA_break_even_lifetime_years"] > 0].copy()

    # Optional: keep only the most important/visible items (top 15 hardest)
    df = df.sort_values("PLA_break_even_lifetime_years", ascending=False).head(15)

    # Plot
    Path("reports/figures").mkdir(parents=True, exist_ok=True)
    out_path = Path("reports/figures/PLA_break_even_lifetime_vs_ABS.png")

    plt.figure()
    plt.bar(df["impact_category"], df["PLA_break_even_lifetime_years"])
    plt.axhline(15, linestyle="--")  # reference lifetime threshold (15 years)
    plt.title("PLA break-even lifetime vs ABS (per impact category)")
    plt.ylabel("Break-even PLA lifetime (years)")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

    print(f"✅ Saved break-even plot: {out_path}")


if __name__ == "__main__":
    main()