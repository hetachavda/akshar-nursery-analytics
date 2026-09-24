"""Run the full pipeline: data -> database -> notebook (with outputs) -> dashboard."""
import runpy
from pathlib import Path

SRC = Path(__file__).resolve().parent
for step in ["generate_data.py", "build_database.py", "build_notebook.py", "build_dashboard.py", "build_assets.py"]:
    print(f"\n=== {step} ===")
    runpy.run_path(str(SRC / step), run_name="__main__")
