#!/usr/bin/python3
import subprocess

#Get Host Name
def host_name():
    try:    
        hostname = subprocess.run(
            "hostnamee",
            capture_output=True,
            text=True,
            check=True
        )
        return hostname.stdout.strip()
    except subprocess.CalledProcessError:
        return "UNKNOWN!"
    except FileNotFoundError as error:
        print (error.strerror)

#Get Disk Usage
def disk_usage():
    disk = subprocess.run(
        ["df", "-h", "--output=pcent", "/"],
        capture_output=True,
        text=True
    )
    disk = disk.stdout.strip().split()

    return int(disk[1].strip("%"))

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

    return round(memory_use)

#Load average
def load_average():
    load = subprocess.run(
        ["cat", "/proc/loadavg"],
        capture_output=True,
        text=True
    )
    load_1min = load.stdout.strip().split()
    return float(load_1min[0]), float(load_1min[1]), float(load_1min[2])

#Count CPU
def count_cpu():
    count_cpu = subprocess.run(
        ["nproc"],
        capture_output=True,
        text=True
    )
    return int(count_cpu.stdout.strip())

#Load Status
def load_status(load, cpus):
    normalized_load = load / cpus
    if normalized_load < 0.70:
        message = "OK!"
    elif normalized_load < 1.00:
        message = "WARNING!"
    else:
        message = "CRITICAL!!!"
    
    return message

#Health Status Message
def health_status(percent):
    if percent < 80:
        message = "OK!"
    elif percent < 90:
        message = "WARNING!"
    else:
        message = "CRITICAL!!!"

    return message

#Count CPU
cpu = count_cpu()

#Checking Disk Usage
disk_percent = disk_usage()
disk_health = health_status(disk_percent)

#Checking Memory Usage
memory_use = memory_usage()
memory_health = health_status(memory_use)

#Checking Load
load_1min, load_5min, load_15min = load_average()
load_status_1min = load_status(load_1min, cpu)
load_status_5min = load_status(load_5min, cpu)
load_status_15min = load_status(load_15min, cpu)

print("=== SERVER HEALTH ===")
print(f"Hostname: {host_name()}")
print(f"CPU count: {cpu}")
print(f"Disk usage: {disk_percent}% {disk_health}")
print(f"Memory usage: {memory_use}% {memory_health}")
print(f"Load average (1 min): {load_1min} {load_status_1min}")
print(f"             (5 min): {load_5min} {load_status_5min}")
print(f"             (15 min): {load_15min} {load_status_15min}")