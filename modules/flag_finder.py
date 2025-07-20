import requests
import colorama
from colorama import Fore, Style
import random
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime

def log_action(message):
    """Log actions/errors to ctf_log.txt"""
    try:
        with open("data/ctf_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except Exception as e:
        print(f"{Fore.RED}[-] Error logging: {e}{Style.RESET_ALL}")

def run_flag_finder(target, mode, stealth_mode, colors):
    """Find CTF flags like a flag-sniping pro"""
    try:
        result = []
        flag_patterns = ["flag{.*}", "HTB{.*}", "THM{.*}"]
        print(f"{colors['success']}[+] Hunting flags in {target}... Let's snag those flags!{Style.RESET_ALL}")
        log_action(f"Starting flag hunt on {target}")
        if target.startswith("http"):
            headers = {'User-Agent': 'CTFBlitz/1.0'}
            r = requests.get(target, headers=headers, timeout=5)
            if stealth_mode:
                time.sleep(random.uniform(0.5, 2))
            text = r.text
            if mode == "Advanced":
                soup = BeautifulSoup(r.text, 'html.parser')
                text += "\n".join([s.get_text() for s in soup.find_all(['script', 'style', 'p'])])
        else:
            if not target.startswith("data/"):
                log_action(f"Invalid file path: {target}")
                return f"{colors['error']}[-] Invalid file path! Use data/ prefix.{Style.RESET_ALL}"
            with open(target) as f:
                text = f.read()
        for pattern in flag_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                result.append(f"Pwned! Found {match}")
        if not result and mode == "Normal":
            result.append(f"No flags found. Try formats: {', '.join(flag_patterns)}")
        log_action(f"Flag hunt completed on {target}")
        return "\n".join(result) or f"{colors['error']}[-] No flags found! Keep hunting!{Style.RESET_ALL}"
    except Exception as e:
        log_action(f"Flag finder error: {e}")
        return f"{colors['error']}[-] Flag finder error: {e}{Style.RESET_ALL}"