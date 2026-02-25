# src/make_plots.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

KEY_CATEGORIES = [
    "climate change - GWP100",
    "fossil depletion - FDP",
    "human toxicity - HTPinf",
]

def main():
    Path("reports/figures").mkdir(parents=True, exist_ok=True)

    master = pd.read_csv("data/processed/master_impacts.csv")
    pla6  = pd.read_csv("data/processed/PLA_DML6.csv").assign(material="PLA (L=6, DM=2.5)")
    pla10 = pd.read_csv("data/processed/PLA_DML10.csv").assign(material="PLA (L=10, DM=1.5)")
    pla15 = pd.read_csv("data/processed/PLA_DML15.csv").assign(material="PLA (L=15, DM=1.0)")

    combined = pd.concat([master, pla6, pla10, pla15], ignore_index=True)

    # Plot: impacts for selected categories
    plot_df = combined[combined["impact_category"].isin(KEY_CATEGORIES)].copy()

    # order materials
    order = ["ABS", "PP", "PLA", "PLA (L=6, DM=2.5)", "PLA (L=10, DM=1.5)", "PLA (L=15, DM=1.0)"]
    plot_df["material"] = pd.Categorical(plot_df["material"], categories=order, ordered=True)
    plot_df = plot_df.sort_values(["impact_category", "material"])

    for cat in KEY_CATEGORIES:
        dfc = plot_df[plot_df["impact_category"] == cat]
        plt.figure()
        plt.bar(dfc["material"].astype(str), dfc["value"])
        plt.title(cat)
        plt.ylabel(dfc["unit"].iloc[0] if len(dfc) else "")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        out = Path("reports/figures") / f"{cat.replace(' ', '_').replace('/', '_')}.png"
        plt.savefig(out, dpi=200)
        plt.close()

    print("✅ Plots saved in reports/figures/")

if __name__ == "__main__":
    main()