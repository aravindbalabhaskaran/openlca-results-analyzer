# src/run_pipeline.py
from pathlib import Path
import subprocess
import sys

def main():
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    Path("reports/figures").mkdir(parents=True, exist_ok=True)

    # Run steps
    subprocess.check_call([sys.executable, "-m", "src.build_master"])
    subprocess.check_call([sys.executable, "-m", "src.reproduce_dm"])
    subprocess.check_call([sys.executable, "-m", "src.make_plots"])

    print("✅ Pipeline complete. Check data/processed and reports/figures")

if __name__ == "__main__":
    main()