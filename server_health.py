#!/usr/bin/python3
import subprocess

def host_name():
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
    return disk.stdout.strip("Use%").split()

print("=== SERVER HEALTH ===")
print(f"Hostname: {host_name()}")
print(f"Disk usage: {disk_usage()}")