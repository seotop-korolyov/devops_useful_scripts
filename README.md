# DevOps Useful Scripts

A collection of Python utilities for common Linux and DevOps administration tasks.

The repository currently contains a server health monitoring script that checks system resources, Docker service status, and Docker container health.

The project is intended both as practical DevOps tooling and as hands-on practice with Python system administration and automation.

## Server Health Monitor

`server_health.py` performs a health check of a Linux server and reports the status of important system resources and Docker containers.

### What It Checks

The script monitors:

* Hostname
* Number of available CPUs
* Root filesystem disk usage
* Memory usage
* 1, 5, and 15 minute system load averages
* Docker service status
* Running Docker containers
* Docker container health status
* Expected but missing containers

## Health Thresholds

### Disk and Memory

The script classifies disk and memory usage as:

| Usage         | Status        |
| ------------- | ------------- |
| Below 80%     | `OK!`         |
| 80–89%        | `WARNING!`    |
| 90% or higher | `CRITICAL!!!` |

### System Load

Load averages are normalized by the number of available CPUs:

| Load per CPU   | Status        |
| -------------- | ------------- |
| Below 0.70     | `OK!`         |
| 0.70–0.99      | `WARNING!`    |
| 1.00 or higher | `CRITICAL!!!` |

## Docker Monitoring

The script checks whether `docker.service` is running using `systemctl`.

It also retrieves running containers and checks their Docker health status.

Possible container states include:

* `HEALTHY`
* `UNHEALTHY`
* `STARTING`
* `NO HEALTHCHECK`

The script can also detect containers that are expected to be running but are missing.

## Expected Containers

The current configuration monitors these containers:

```text
parser-web-1
parser-php-1
parser-phpmyadmin-1
repositry-nginx-1
repositry-registry-1
```

These values can be changed in the `expected_containers` set inside `server_health.py` to match another server environment.

## Requirements

The script is designed for a Linux system with:

* Python 3
* `systemd`
* Docker
* Standard Linux utilities such as:

  * `df`
  * `free`
  * `nproc`
  * `hostname`

Docker must be installed if Docker monitoring is required.

Writing to `/var/log/server_health.log` also requires appropriate filesystem permissions.

## Usage

Make the script executable:

```bash
chmod +x server_health.py
```

Run it directly:

```bash
./server_health.py
```

or with Python:

```bash
python3 server_health.py
```

## Example Output

```text
=== SERVER HEALTH ===
Hostname: server01
CPU count: 4
Disk usage: 42% OK!
Memory usage: 51% OK!
Load average (1 min): 0.35 OK!
             (5 min): 0.28 OK!
             (15 min): 0.24 OK!
Docker service:  [ RUNNING ]

=== RUNNING CONTAINERS ===
parser-web-1          [ HEALTHY ]
parser-php-1          [ HEALTHY ]

=== MISSING CONTAINERS ===

=== SUMMARY ===
Overall status: [ HEALTHY ]
```

## Exit Codes

The script uses exit codes so that it can also be integrated with other automation or monitoring tools.

* `0` — health check completed without a critical condition
* `1` — a critical condition was detected

A critical result can occur when:

* disk usage reaches the critical threshold
* memory usage reaches the critical threshold
* normalized system load reaches the critical threshold
* Docker is not running
* Docker container information cannot be retrieved
* a container is unhealthy
* an expected container is missing

## Logging

When a critical condition is detected, the script appends information to:

```text
/var/log/server_health.log
```

The log includes information about disk usage, memory usage, system load, Docker status, unhealthy containers, and missing containers.

## Python Concepts Used

This project uses several Python concepts in a practical system-administration context:

* Functions
* Sets, lists, and dictionaries
* Conditional logic
* Exception handling
* `subprocess`
* Process exit codes
* File operations
* Date and time handling
* Parsing Linux command output
* Integration with Linux system commands
* Integration with Docker CLI commands

## Future Improvements

Possible future improvements include:

* Moving configuration to a separate file
* Making expected container names configurable
* Adding command-line arguments with `argparse`
* Configurable warning and critical thresholds
* Improved logging with Python's `logging` module
* Network and service checks
* Automatic notifications
* Unit tests
* Additional DevOps administration scripts

## Purpose

This repository is part of my practical DevOps learning.

The goal is to build useful automation tools while developing skills in Python, Linux system administration, Docker, monitoring, troubleshooting, and scripting.
