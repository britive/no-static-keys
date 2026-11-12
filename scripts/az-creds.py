#!/usr/bin/env python3
"""Turn `pybritive checkout -m json` output for an Azure profile into an env file.

Exits non-zero unless TenantId, ClientId AND ClientSecret are all present:
Britive returns the secret only when it mints a new service principal, so a
payload that parses but has an empty secret is a failed checkout.

Usage: az-creds.py <checkout-output> <env-file-to-write>
"""
import json
import shlex
import sys

try:
    raw = open(sys.argv[1], encoding="utf-8").read()
    data, _ = json.JSONDecoder().raw_decode(raw[raw.index("{"):])
except (ValueError, OSError):
    sys.exit(2)
fields = {"AZ_TENANT": "TenantId", "AZ_CLIENT": "ClientId", "AZ_SECRET": "ClientSecret"}
if not all(data.get(v) for v in fields.values()):
    sys.exit(1)
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for env, key in fields.items():
        f.write(f"{env}={shlex.quote(data[key])}\n")
