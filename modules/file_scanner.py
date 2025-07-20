import requests
import colorama
from colorama import Fore, Style
import random
import time
import os
from datetime import datetime

def log_action(message):
    """Log actions/errors to ctf_log.txt"""
    try:
        with open("data/ctf_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except Exception as e:
        print(f"{Fore.RED}[-] Error logging: {e}{Style.RESET_ALL}")

def run_file_scanner(url, mode, stealth_mode, colors):
    """Scan for hidden files like a CTF pro"""
    try:
        result = []
        headers = {'User-Agent': 'CTFBlitz/1.0'}
        files = ["robots.txt", "flag.txt", "admin", "login", "config"] if mode == "Normal" else []
        if mode == "Advanced":
            if not os.path.exists("data/common.txt"):
                log_action("data/common.txt not found")
                return f"{colors['error']}[-] data/common.txt not found! Download from dirb.{Style.RESET_ALL}"
            with open("data/common.txt") as f:
                files = f.read().splitlines()
                if not files:
                    log_action("data/common.txt is empty")
                    return f"{colors['error']}[-] data/common.txt is empty!{Style.RESET_ALL}"
        extensions = [".bak", ".txt", ".zip"] if mode == "Advanced" else []
        print(f"{colors['success']}[+] Scanning {url} for hidden files... Digging for gold!{Style.RESET_ALL}")
        log_action(f"Starting file scan on {url}")
        for f in files[:100]:
            try:
                r = requests.get(f"{url}/{f}", headers=headers, timeout=5)
                if stealth_mode:
                    time.sleep(random.uniform(0.5, 2))
                if r.status_code == 200:
                    result.append(f"Pwned! Found /{f} (200 OK)—flag city!")
                    if mode == "Advanced":
                        for ext in extensions:
                            r_ext = requests.get(f"{url}/{f}{ext}", headers=headers, timeout=5)
                            if stealth_mode:
                                time.sleep(random.uniform(0.5, 2))
                            if r_ext.status_code == 200:
                                result.append(f"Pwned! Found /{f}{ext} (200 OK)—sneaky file!")
            except:
                continue
        log_action(f"File scan completed on {url}")
        return "\n".join(result) or f"{colors['error']}[-] No files found! Try another path!{Style.RESET_ALL}"
    except Exception as e:
        log_action(f"File scanner error: {e}")
        return f"{colors['error']}[-] File scanner error: {e}{Style.RESET_ALL}"