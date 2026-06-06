import socket #core library- raw TCP connections
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime #timestamp

def grab_banner(sock): #send min HTTP req
    try:
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip() #response-bytes = skip
        return banner if banner else None
    except:
        return None
    

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = IPv4, SOCK_STREAM = TCP
        sock.settimeout(timeout) #1 sec per port
        result = sock.connect_ex((host, port))
        if result == 0: #success- port open
            banner = grab_banner(sock)
            sock.close()
            return (port, True, banner) #grab banner
        else:
            sock.close()
            return (port, False, None)
    except socket.error:
        return (port, False, None)
    
def run_scan(host, start_port, end_port, threads=100, timeout=1):
    print(f"\n[*] Starting scan on {host}")
    print(f"[*] Port range: {start_port}-{end_port}")
    print(f"[*] Threads: {threads}")
    print(f"[*] Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    open_ports = []
    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, host, port, timeout): port for port in ports}
        for future in as_completed(futures):
            port, is_open, banner = future.result()
            if is_open:
                if banner:
                    print(f"[+] Port {port}/tcp OPEN — Banner: {banner[:80]}") #capped at 80 chars
                else:
                    print(f"[+] Port {port}/tcp OPEN")
                open_ports.append((port, banner))

    open_ports.sort(key=lambda x: x[0]) #sorted by port num
    return open_ports


def main(): #CLI interface for user
    parser = argparse.ArgumentParser(description="Threaded TCP port scanner with banner grabbing")
    parser.add_argument("host", help="Target host or IP (e.g. scanme.nmap.org)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout per port in seconds (default: 1.0)")
    args = parser.parse_args()

    if args.start < 1 or args.end > 65535 or args.start > args.end: #limits nonsense input
        print("[-] Invalid port range. Ports must be between 1-65535 and start must be less than end.")
        sys.exit(1)

    try: #resolves hostname to IP (handles IP and hostanme)
        host_ip = socket.gethostbyname(args.host)
        print(f"[*] Resolved {args.host} to {host_ip}")
    except socket.gaierror:
        print(f"[-] Could not resolve host: {args.host}")
        sys.exit(1)

    results = run_scan(host_ip, args.start, args.end, args.threads, args.timeout)

    print(f"\n[*] Scan complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] {len(results)} open port(s) found\n")
    if results:
        print("--- Summary ---")
        for port, banner in results:
            if banner:
                print(f"  {port}/tcp — {banner[:80]}")
            else:
                print(f"  {port}/tcp — no banner")

if __name__ == "__main__":
    main()

