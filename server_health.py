#!/usr/bin/python3
import subprocess

#Get Host Name
def host_name():
    hostname = subprocess.run(
        "hostname",
        capture_output=True,
        text=True
    )

    return hostname.stdout.strip()

#Get Disk Usage
def disk_usage():
    disk = subprocess.run(
        ["df", "-h", "--output=pcent", "/"],
        capture_output=True,
        text=True
    )
    disk = disk.stdout.strip().split()
    disk_int = int(disk[1].strip("%"))

    return disk_int

#Check Memory
def memory_usage():
    memory = subprocess.run(
        ["free", "-m"],
        capture_output=True,
        text=True
    )
    memory_line = memory.stdout.splitlines()[1]
    memory_data = memory_line.split()
    memory_use = (int(memory_data[1]) - int(memory_data[6]))/int(memory_data[1]) * 100
    memory_use = round(memory_use)

    return memory_use

def health_status(percent):
    if percent < 80:
        message = "OK!"
    elif percent < 90:
        message = "WARNING!"
    else:
        message = "CRITICAL!!!"

    return message

#Checking Disk Usage
disk_percent = disk_usage()
disk_health = health_status(disk_percent)

#Checking Memory Usage
memory_use = memory_usage()
memoty_health = health_status(memory_use)


print("=== SERVER HEALTH ===")
print(f"Hostname: {host_name()}")
print(f"Disk usage: {disk_percent}% {disk_health}")
print(f"Memory usage: {memory_use}% {memoty_health}")