"""Write uae_hr/translations/ar.csv from dev/ar_source.py, then report coverage.

Run from the repo root: python3 dev/build_translations.py
"""

import csv
import importlib.util
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(path, name):
	spec = importlib.util.spec_from_file_location(name, path)
	mod = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(mod)
	return mod


law = load(ROOT / "uae_hr" / "law.py", "law")
src = load(ROOT / "dev" / "ar_source.py", "ar_source")
rows = {**src.AR, **src.law_rows(law)}
target = ROOT / "uae_hr" / "translations" / "ar.csv"
target.parent.mkdir(exist_ok=True)
with open(target, "w", newline="", encoding="utf-8") as fh:
	w = csv.writer(fh, lineterminator="\n")
	for en in sorted(rows):
		w.writerow([en, rows[en]])
print(f"wrote {len(rows)} rows to {target.relative_to(ROOT)}")
sys.exit(subprocess.call([sys.executable, str(ROOT / "dev" / "extract_messages.py"), "--missing"]))
