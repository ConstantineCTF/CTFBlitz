import requests
import colorama
from colorama import Fore, Style
import random
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime

def log_action(message):
    """Log actions/errors to ctf_log.txt"""
    try:
        with open("data/ctf_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except Exception as e:
        print(f"{Fore.RED}[-] Error logging: {e}{Style.RESET_ALL}")

def run_web_vuln(url, mode, stealth_mode, colors):
    """Run web vulnerability scan like Burp Suite"""
    try:
        result = []
        headers = {'User-Agent': 'CTFBlitz/1.0'}
        print(f"{colors['success']}[+] Scanning {url} for vulns... Time to pwn the web!{Style.RESET_ALL}")
        log_action(f"Starting Web Vuln scan on {url}")
        r = requests.get(url, headers=headers, timeout=5)
        if stealth_mode:
            time.sleep(random.uniform(0.5, 2))
        # Check headers
        if mode == "Normal":
            critical_headers = {
                'X-Frame-Options': 'Clickjacking risk—hackable!',
                'Content-Security-Policy': 'XSS risk—script kiddie alert!',
                'X-Content-Type-Options': 'MIME sniffing risk—sneaky!'
            }
            for header, risk in critical_headers.items():
                if header not in r.headers:
                    result.append(f"Missing {header}: {risk}")
        # Check paths
        paths = ["admin", "login", "robots.txt", "flag.txt"] if mode == "Normal" else []
        if mode == "Advanced":
            if not os.path.exists("data/common.txt"):
                log_action("data/common.txt not found")
                return f"{colors['error']}[-] data/common.txt not found! Download from dirb.{Style.RESET_ALL}"
            with open("data/common.txt") as f:
                paths = f.read().splitlines()
                if not paths:
                    log_action("data/common.txt is empty")
                    return f"{colors['error']}[-] data/common.txt is empty!{Style.RESET_ALL}"
        for path in paths[:100]:
            try:
                r_path = requests.get(f"{url}/{path}", headers=headers, timeout=5)
                if stealth_mode:
                    time.sleep(random.uniform(0.5, 2))
                if r_path.status_code == 200:
                    result.append(f"Found /{path} (200 OK)—potential flag hideout!")
            except:
                continue
        # Crawl in Advanced mode
        if mode == "Advanced":
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a', href=True)[:10]:
                href = link['href']
                if href.startswith('/'):
                    try:
                        r_link = requests.get(f"{url}{href}", headers=headers, timeout=5)
                        if stealth_mode:
                            time.sleep(random.uniform(0.5, 2))
                        if r_link.status_code == 200:
                            result.append(f"Found {href} (200 OK)—sneaky link!")
                    except:
                        continue
        log_action(f"Web Vuln scan completed on {url}")
        return "\n".join(result) or f"{colors['error']}[-] No vulns or paths found!{Style.RESET_ALL}"
    except Exception as e:
        log_action(f"Web vuln error: {e}")
        return f"{colors['error']}[-] Web vuln error: {e}{Style.RESET_ALL}"