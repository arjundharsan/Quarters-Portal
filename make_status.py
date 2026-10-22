"""Build status.json (hashed IDs) and publish allotment orders under hashed file names.

Usage (run from the repo root):
  python tools/make_status.py tools/status.csv > status.json

Put each allotment order PDF in tools/orders_src/ named EMPLOYEEID.pdf (e.g. E1002.pdf).
The script copies it to orders/<hash>.pdf and links it in status.json.
SALT must match the SALT value in index.html."""
import csv, hashlib, json, os, shutil, sys
SALT = "change-this-salt"
SRC, DST = "tools/orders_src", "orders"
os.makedirs(DST, exist_ok=True)
out = {}
for r in csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8")):
    eid = r["employee_id"].strip().upper()
    h = hashlib.sha256((SALT + eid).encode()).hexdigest()
    entry = {"stage": r["stage"].strip(), "quarters": r.get("quarters", "").strip()}
    src = os.path.join(SRC, eid + ".pdf")
    if os.path.exists(src):
        name = h[:24] + ".pdf"
        shutil.copyfile(src, os.path.join(DST, name))
        entry["order"] = DST + "/" + name
    out[h] = entry
json.dump(out, sys.stdout, indent=1)
