# Python Port Scanner

A beginner Python port scanner built as part of a self-directed cybersecurity learning pathway.

Scans ports 1–1000 on a target IP address, identifies open ports, maps them to common service names, and saves the results to a text file.

---

## What it does

- Accepts a target IP address as input with basic validation
- Scans ports 1 to 1000 using TCP connection attempts
- Identifies common services by port number (FTP, SSH, HTTP, SMB, etc.)
- Prints open ports to the terminal in real time
- Saves all results to `scan_results.txt`

---

## Example output

```
Scan results for 192.168.100.238
==============================
Port 21 is open -- FTP
Port 22 is open -- SSH
Port 23 is open -- Telnet
Port 25 is open -- SMTP
Port 53 is open -- DNS
Port 80 is open -- HTTP
Port 111 is open -- RPCbind
Port 139 is open -- NetBIOS
Port 445 is open -- SMB
Port 512 is open -- rexec
Port 513 is open -- rlogin
Port 514 is open -- rsh
```

*Output above from a scan against Metasploitable 2 running in an isolated VirtualBox lab environment.*

---

## How to run it

**Requirements:** Python 3 (no external libraries needed, uses the built-in `socket` module only)

```bash
python portScanner_01.py
```

You will be prompted to enter a target IP address.

---

## How it works

The scanner uses Python's built-in `socket` library to attempt a TCP connection to each port in the range 1–1000. If the connection succeeds (returns 0), the port is open. A 1-second timeout is applied to each connection to avoid hanging on filtered ports.

Open ports are matched against a dictionary of common port-to-service mappings and the result is written to both the terminal and a results file.

---

## Disclaimer

This tool is for **educational use and authorised testing only**. Only run it against systems you own or have explicit written permission to scan. Scanning systems without authorisation may be illegal under the Computer Misuse Act 1990 (UK) and equivalent laws in other jurisdictions.

This was built and tested against Metasploitable 2 in an isolated home lab environment.

---

## Part of a wider project
Future version will add threading for faster scans, banner grabbing to identify software versions, and CSV export.
