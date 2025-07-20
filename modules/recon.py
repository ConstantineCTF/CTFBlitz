import nmap
import colorama
from colorama import Fore, Style
import random
import time
import re
from datetime import datetime

def log_action(message):
    """Log actions/errors to ctf_log.txt"""
    try:
        with open("data/ctf_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except Exception as e:
        print(f"{Fore.RED}[-] Error logging: {e}{Style.RESET_ALL}")

def run_recon(ip, mode, stealth_mode, colors):
    """Run port and service scan with Nmap"""
    try:
        nm = nmap.PortScanner()
        result = []
        if mode == "Normal":
            port_range = input(f"{colors['input']}Port range (e.g., 80-100) or Enter for top 100: {Style.RESET_ALL}").strip() or "top 100"
            if port_range == "top 100":
                args = "-sS -F"
            else:
                if not re.match(r"^\d+-\d+$", port_range) or not (1 <= int(port_range.split('-')[0]) <= int(port_range.split('-')[1]) <= 65535):
                    log_action(f"Invalid port range: {port_range}")
                    return f"{colors['error']}[-] Invalid port range! Use format 80-100, ports 1-65535.{Style.RESET_ALL}"
                args = f"-sS -p {port_range}"
        else:
            args = "-sS -sV -O --script=vuln -p-"
        if stealth_mode:
            args += " -T2"
        print(f"{colors['success']}[+] Running {mode} Recon on {ip}... Scanning like a pro!{Style.RESET_ALL}")
        log_action(f"Starting {mode} Recon on {ip} with args: {args}")
        nm.scan(ip, arguments=args)
        if stealth_mode:
            time.sleep(random.uniform(0.5, 2))
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]['state']
                    service = nm[host][proto][port].get('name', 'unknown')
                    result.append(f"Port {port}/{proto}: {state} ({service})")
                    if mode == "Advanced":
                        scripts = nm[host][proto][port].get('script', {})
                        for script, output in scripts.items():
                            result.append(f"Vuln Script {script}: {output[:100]}...")
        log_action(f"Recon completed on {ip}")
        return "\n".join(result) or f"{colors['error']}[-] No open ports found!{Style.RESET_ALL}"
    except Exception as e:
        log_action(f"Recon error: {e}")
        return f"{colors['error']}[-] Recon error: {e}{Style.RESET_ALL}"