#!/usr/bin/env python3
import socket
import subprocess
import sys

host = "drive.google.com"

print("=== Python socket.getaddrinfo ===")
try:
    ai = socket.getaddrinfo(host, 443)
    print("OK: getaddrinfo returned", len(ai), "entries; sample:", ai[:3])
except Exception as e:
    print("ERROR:", repr(e))

print()
print("=== nslookup drive.google.com ===")
try:
    proc = subprocess.run(["nslookup", host], capture_output=True, text=True)
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print("nslookup exit", proc.returncode, "stderr:", proc.stderr.strip())
except Exception as e:
    print("nslookup error:", repr(e))

print()
print("=== ping -c 4 drive.google.com ===")
try:
    proc = subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True)
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print("ping exit", proc.returncode, "stderr:", proc.stderr.strip())
except Exception as e:
    print("ping error:", repr(e))

# Optional: try a simple HTTPS request using requests if available
print()
print("=== simple HTTPS HEAD request (requests) ===")
try:
    import requests
    try:
        r = requests.head("https://drive.google.com", timeout=5)
        print("requests HEAD status:", r.status_code)
    except Exception as e:
        print("requests error:", repr(e))
except Exception:
    print("requests not installed in venv; skipping HTTPS check")
