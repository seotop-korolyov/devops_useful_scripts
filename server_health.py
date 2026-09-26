#!/usr/bin/python3
import subprocess, sys
from datetime import datetime

#Clean Screen
subprocess.run(["clear"])

#Global Variable
exit_code = 0
container_statuses_log = {}
path_log_file = "/var/log/server_health.log"

#Expected Containers
expected_containers = {
    "parser-web-1",
    "parser-php-1",
    "parser-phpmyadmin-1",
    "repositry-nginx-1",
    "repositry-registry-1"
}

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

#Missing Containers
def missing_containers(expected_containers, running_conrainers):
    #for container in expected_containers:
    print(expected_containers, running_conrainers)

#Logs
def write_log(status):
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path_log_file, "a") as log_file:
        log_file.write(f"{data} Disk: {status['Disk']} \
Memory: {status['Memory']} \
Load: {status['Load']} \
Docker: {status['Docker']} \
Unhealthy containers: {status['Containers']}\
\n")

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
disk_metric = format_metric(disk_percent, disk_health, '%')

#Checking Memory Usage
memory_use = memory_usage()
memory_health = health_status(memory_use)
memory_metric = format_metric(memory_use, memory_health, '%')

#Checking Load
load_1min, load_5min, load_15min = load_average()
load_status_1min = load_status(load_1min, cpu)
load_metric = format_metric(load_1min, load_status_1min)
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
print(f"Disk usage: {disk_metric}")
print(f"Memory usage: {memory_metric}")
print(f"Load average (1 min): {load_metric}")
print(f"             (5 min): {format_metric(load_5min, load_status_5min)}")
print(f"             (15 min): {format_metric(load_15min, load_status_15min)}")
print(f"Docker service:  [ {docker} ]")
print("\n")
print("=== RUNNING CONTAINERS ===")
if containers is None:
    print("UNKNOWN")
elif containers:
    for container in containers:
        container_status = container_health(container)
        if container_status == "UNHEALTHY":
            container_statuses_log[container] = container_status
        print(f"{container} \t [ {container_status} ]")
else:
    print("No running containers")
print("\n")
missing_containers(expected_containers, containers)
print("=== MISSING CONTAINERS ===")

print("\n")


#Exit Code
statuses = [
    disk_health,
    memory_health,
    load_status_1min,
    load_status_5min,
    load_status_15min
]

if any(status == "CRITICAL!!!" for status in statuses) \
    or docker == "NOT RUNNING" \
    or any(container_status == "UNHEALTHY" for container_status in container_statuses_log.values()):
    exit_code = 1
    print("=== SUMMARY ===")
    print("Overall status: [ CRITICAL!!! ]")
    write_log({"Disk": disk_metric,
               "Memory": memory_metric,
               "Load": load_metric,
               "Docker": docker, 
               "Containers": ", ".join(container_statuses_log.keys())
               })
else:
    print("=== SUMMARY ===")
    print("Overall status: [ HEALTHY ]")
print("\n\n")
sys.exit(exit_code)