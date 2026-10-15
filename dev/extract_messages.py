"""List every user-facing string and check uae_hr/translations/ar.csv covers it.

Run from the repo root: python3 dev/extract_messages.py [--missing]

Sources: doctype labels, descriptions and Select options; custom fields; _() and __() calls;
seeded record names; the report and workspace labels. The DL 66 rule (Arabic prevails) is why the
app ships Arabic from day one.
"""

import ast
import csv
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "uae_hr"


def load(path, name):
	spec = importlib.util.spec_from_file_location(name, path)
	mod = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(mod)
	return mod


def from_doctypes(out):
	for path in (APP / "uae_hr" / "doctype").glob("*/*.json"):
		d = json.loads(path.read_text())
		out.add(d["name"])
		for f in d["fields"]:
			for key in ("label", "description"):
				if f.get(key):
					out.add(f[key])
			if (
				f["fieldtype"] == "Select"
				and f.get("options")
				and f["fieldname"] not in ("naming_series", "document_field")
			):
				out.update(o for o in f["options"].split("\n") if o)


def from_custom_fields(out):
	tree = ast.parse((APP / "setup" / "custom_fields.py").read_text())
	for node in ast.walk(tree):
		if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "cf":
			args = [a.value for a in node.args if isinstance(a, ast.Constant)]
			if len(args) >= 3:
				out.add(args[2])
			for kw in node.keywords:
				if kw.arg == "description" and isinstance(kw.value, ast.Constant):
					out.add(kw.value.value)
				if kw.arg == "options" and isinstance(kw.value, ast.Constant) and "\n" in kw.value.value:
					out.update(o for o in kw.value.value.split("\n") if o)
		if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "MIRROR_NOTE":
			out.add(node.value.value)
			out.add(node.value.value + " (Passport)")


def from_calls(out):
	"""_() in Python via ast (adjacent literals are one string to Python, and to Frappe), __() in JS by regex."""
	for path in APP.rglob("*.py"):
		if "tests" in path.parts:
			continue
		for node in ast.walk(ast.parse(path.read_text())):
			if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "_" and node.args:
				if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
					out.add(node.args[0].value)
	for path in APP.rglob("*.js"):
		for m in re.finditer(r'(?<![\w.])__\(\s*"((?:[^"\\]|\\.)*)"', path.read_text()):
			out.add(m.group(1).replace('\\"', '"'))


def from_seeds(out):
	tree = ast.parse((APP / "setup" / "masters.py").read_text())
	for node in ast.walk(tree):
		if (
			isinstance(node, ast.Assign)
			and isinstance(node.targets[0], ast.Name)
			and node.targets[0].id.isupper()
		):
			name = node.targets[0].id
			value = ast.literal_eval(node.value)
			if name == "PERMIT_TYPES":
				for p in value:
					out.add(p[0])
					if p[2]:
						out.add(p[2])
			elif name == "DOCUMENT_TYPES":
				out.update(d[0] for d in value)
			elif name == "ISSUED_ITEM_TYPES":
				out.update(value)
	out.update(
		(
			"Basic",
			"Housing Allowance",
			"Transport Allowance",
			"Other Allowance",
			"UAE PRO",
			"UAE HR",
			"Expiring Documents",
		)
	)
	for path in (APP / "workspace_sidebar").glob("*.json"):
		out.update(i["label"] for i in json.loads(path.read_text())["items"])
	for path in (APP / "uae_hr" / "workspace").glob("*/*.json"):
		w = json.loads(path.read_text())
		out.update(link["label"] for link in w["links"])
		out.update(s["label"] for s in w["shortcuts"])


def collect():
	out = set()
	from_doctypes(out)
	from_custom_fields(out)
	from_calls(out)
	from_seeds(out)
	return {s for s in out if s.strip() and not s.startswith("<div")}


def existing():
	path = APP / "translations" / "ar.csv"
	if not path.exists():
		return {}
	with open(path, newline="", encoding="utf-8") as fh:
		return {row[0]: row[1] for row in csv.reader(fh) if row}


if __name__ == "__main__":
	strings = collect()
	have = existing()
	missing = sorted(strings - set(have))
	stale = sorted(set(have) - strings)
	if "--missing" in sys.argv:
		for s in missing:
			print(json.dumps(s, ensure_ascii=False))
	print(
		f"{len(strings)} strings, {len(have)} translated, {len(missing)} missing, {len(stale)} unused",
		file=sys.stderr,
	)
	sys.exit(1 if missing else 0)
