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
    disk = disk.stdout.strip().split()
    disk_int = int(disk[1].strip("%"))
    return disk_int

print("=== SERVER HEALTH ===")
print(f"Hostname: {host_name()}")
print(f"Disk usage: {disk_usage()}%")