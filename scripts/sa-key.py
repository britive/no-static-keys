#!/usr/bin/env python3
"""Turn `pybritive checkout -m json` output for a GCP profile into a key file.

Britive returns the service-account key either as the key JSON itself or as
{"<sa-email>": "<key JSON as a string>"}. Both are normalised here.

Usage: sa-key.py <checkout-output> <key-file-to-write>
"""
import json
import sys

raw = open(sys.argv[1], encoding="utf-8").read()
data, _ = json.JSONDecoder().raw_decode(raw[raw.index("{"):])
if "private_key" not in data:
    value = next(iter(data.values()))
    data = json.loads(value) if isinstance(value, str) else value
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(data, f)
print("service account:", data["client_email"])
