#!/usr/bin/python3
import subprocess

def host_mane():
    hostname = subprocess.run(
        "hostname",
        capture_output=True,
        text=True
    )
    hostname = hostname.stdout.strip()
    return hostname

def disk_usage():
    disk = subprocess.run(
        ["df", "-h", "--output=pcent", "/"],
        capture_output=True,
        text=True
    )
    disk = disk.stdout.strip("Use%")
    return disk

print("=== SERVER HEALTH ===")
print(f"Hostname: {host_mane()}")
print(f"Disk usage: {disk_usage()}")