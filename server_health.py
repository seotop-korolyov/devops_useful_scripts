#!/usr/bin/python3
import subprocess, sys

#Clean Screen
subprocess.run(["clear"])

#Global Variable
exit_code = 0

#Run Command
def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

#Service Status
def service_status(service):
    try:
        status = subprocess.run(
            ["systemctl", "status", service],
            capture_output=True,
            text=True
        )
        if status.returncode == 0:
            message = "RUNNING"
        elif status.returncode == 3:
            message = "NOT RUNNING"
        elif status.returncode == 4:
            message = "NOT FOUND"
        else:
            message = "UNKNOWN"
        return message
    except FileNotFoundError:
        return None

#Get Host Name
def host_name():
    return run_command(["hostname"])

#Get Disk Usage
def disk_usage():
    disk = run_command(["df", "-h", "--output=pcent", "/"])
    if disk is None:
        return None

    disk = disk.strip().split()
    return int(disk[1].strip("%"))

#Check Memory
def memory_usage():
    memory = run_command(["free", "-m"])
    if memory is None:
        return None
    memory_line = memory.splitlines()[1]
    memory_data = memory_line.split()
    memory_use = (int(memory_data[1]) - int(memory_data[6]))/int(memory_data[1]) * 100

    return round(memory_use)

#Load average
def load_average():
    load = run_command(["cat", "/proc/loadavg"])
    if load is None:
        return None, None, None
    load_1min = load.strip().split()
    return float(load_1min[0]), float(load_1min[1]), float(load_1min[2])

#Count CPU
def count_cpu():
    cpu_count = run_command(["nproc"])
    if cpu_count is None:
        return None
    return int(cpu_count.strip())

#Load Status
def load_status(load, cpus):
    if load is None or cpus is None:
        return None
        
    normalized_load = load / cpus
    if normalized_load < 0.70:
        message = "OK!"
    elif normalized_load < 1.00:
        message = "WARNING!"
    else:
        message = "CRITICAL!!!"
    
    return message

#Docker Containers
def docker_containers():
    containers = run_command(["docker", "ps", "--format", "{{.Names}}"])
    if containers is None:
        return None
    return containers.splitlines()

#Containers health check
def container_health(container):
    health = run_command(["docker", "inspect", "--format", '{{.State.Health.Status}}', container])
    if health == "healthy":
        message = "HEALTHY"
    elif health == "unhealthy":
        message = "UNHEALTHY"
    elif health == "starting":
        message = "STARTING"
    elif health is None:
        message = "NO HEALTHCHECK"
    else:
        message = "NO HEALTHCHECK"
    return message

#Health Status Message
def health_status(percent):
    if percent is None:
        return "UNKNOWN!"
    if percent < 80:
        message = "OK!"
    elif percent < 90:
        message = "WARNING!"
    else:
        message = "CRITICAL!!!"

    return message

#Format metric
def format_metric(value, status, unit=""):
    if value is None or status is None:
        return "UNKNOWN!"

    return f"{value}{unit} {status}"

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

#Docker Service check
docker = service_status("docker.service")
if docker is None:
    docker = "UNKNOWN"

#Docker Containers
containers = docker_containers()

print("=== SERVER HEALTH ===")
print(f"Hostname: {host_name()}")
print(f"CPU count: {format_metric(cpu, '')}")
print(f"Disk usage: {format_metric(disk_percent, disk_health, '%')}")
print(f"Memory usage: {format_metric(memory_use, memory_health, '%')}")
print(f"Load average (1 min): {format_metric(load_1min, load_status_1min)}")
print(f"             (5 min): {format_metric(load_5min, load_status_5min)}")
print(f"             (15 min): {format_metric(load_15min, load_status_15min)}")
print(f"Docker service:  [ {docker} ]")
print("\n")
print("=== RUNNING CONTAINERS ===")
if containers is None:
    print("UNKNOWN")
elif containers:
    for container in containers:
        print(f"{container} \t [ {container_health(container)} ]")
else:
    print("No running containers")
print("\n\n")

#Exit Code
if disk_health or memory_health == "CRITICAL!!!":
    exit_code = 1
sys.exit(exit_code)