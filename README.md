# Python Port Scanner

A TCP port scanner built across two versions to show progression — from a simple single-threaded scanner to a threaded tool that grabs service banners from open ports. Both built using Python's standard library only.

---

## What This Tool Does

It tries to connect to each port on a target over TCP. If the connection succeeds, the port is open. Version 2 goes further — once a port is open, it reads whatever the service sends back first. Most services announce themselves immediately with their name and version. That first message is the banner, and it tells you exactly what's running without any guessing.

**v1** does the basics — scans ports 1–1000, maps open ports to known service names, saves results to a file.

**v2** adds threading (scanning hundreds of ports at once instead of one at a time), banner grabbing, hostname resolution, and a full CLI so you can configure the port range, thread count, and timeout from the command line.

---

## Concepts Demonstrated

- TCP sockets and how a connection attempt works
- Threading and concurrency with `ThreadPoolExecutor`
- Banner grabbing and service fingerprinting
- Port-to-service mapping
- CLI argument parsing with `argparse`
- Timeout handling for filtered and unresponsive ports

---

## Requirements

No external libraries needed — both versions use Python's standard library only.

---

## Usage

**v1**
```bash
python portScanner_01.py
```
Prompts for a target IP address.

**v2**
```bash
# Default scan, ports 1-1024
python portScanner_advanced.py scanme.nmap.org

# Custom port range with more threads
python portScanner_advanced.py scanme.nmap.org -s 1 -e 500 -t 200

# Faster scan with reduced timeout
python portScanner_advanced.py scanme.nmap.org -s 1 -e 1024 --timeout 0.5

# Save output to file
python portScanner_advanced.py scanme.nmap.org > results.txt
```

`scanme.nmap.org` is a host maintained by Nmap and explicitly set up for this kind of testing — the equivalent of `zonetransfer.me` for port scanning.

---

## Results

**v1** scanned a local Metasploitable 2 machine and found 12 open ports — FTP, SSH, Telnet, SMTP, NetBIOS, SMB, and several legacy remote shell services (rexec, rlogin, rsh). Metasploitable is a deliberately vulnerable VM used for exactly this kind of lab testing.

**v2** scanned `scanme.nmap.org` across ports 1–1024 in 2 seconds with 100 threads and found 2 open ports. Banner grabbing confirmed port 22 is running `OpenSSH 6.6.1` on Ubuntu and port 80 is running `Apache 2.4.7`. The 200-thread run completed the same scan in 1 second. The reduced timeout run returned identical results — faster but with a higher chance of missing slow-responding services.

---

## Files

| File | Description |
|------|-------------|
| `portScanner_01.py` | v1 — single-threaded, IP input, service name mapping |
| `portScanner_advanced.py` | v2 — threaded, banner grabbing, CLI flags |
| `scan_results.txt` | v1 output — scan against Metasploitable 2 |
| `scan_ports_1-1024.txt` | v2 default run — ports 1-1024, 100 threads |
| `custom_range_more_threads.txt` | v2 — ports 1-500, 200 threads |
| `timeout_flag.txt` | v2 — ports 1-1024, 0.5s timeout |
