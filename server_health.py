#!/usr/bin/python3
import subprocess

result = subprocess.run(
    "hostname",
    capture_output=True,
    text=True
)

hostname = result.stdout.strip()
print("=== SERVER HEALTH ===")
print(f"Hostname: {hostname}")