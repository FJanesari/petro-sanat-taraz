#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate nginx redirect map from CSV - Regex version
"""
import csv
import os
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGINX_DIR = os.path.join(ROOT, "nginx")
CSV_PATH = os.path.join(NGINX_DIR, "redirects.csv")
MAP_OUT = os.path.join(NGINX_DIR, "redirects_map.conf")

if not os.path.isfile(CSV_PATH):
    print("❌ CSV file not found:", CSV_PATH)
    sys.exit(1)

pairs = []


def path_only(u):
    if u.startswith(("http://", "https://")):
        parsed = urlparse(u)
        return parsed.path or "/"
    return u


with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader, None)

    for row in reader:
        if len(row) < 2:
            continue
        new_raw, old_raw = row[0].strip(), row[1].strip()
        if not old_raw or not new_raw:
            continue

        old = path_only(old_raw)
        new = path_only(new_raw)
        if not old.startswith("/"):
            old = "/" + old
        if not new.startswith("/"):
            new = "/" + new

        pairs.append((old, new))

seen = set()
uniq = []
for o, n in pairs:
    if o in seen:
        continue
    seen.add(o)
    uniq.append((o, n))

# تولید فایل map با ~ برای regex
with open(MAP_OUT, "w", encoding="utf-8") as f:
    f.write("# Auto-generated nginx redirect map\n")
    f.write("map $request_uri $redirect_uri {\n")
    f.write("    default \"\";\n")
    for old, new in uniq:
        f.write(f"    ~^{old}$ {new};\n")
    f.write("}\n")

print("✅ Regex Map file generated successfully!")
print("📁 Output file:", MAP_OUT)
print("🔢 Total redirects:", len(uniq))
