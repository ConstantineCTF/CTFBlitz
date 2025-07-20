import colorama
from colorama import Fore, Style
import json
import random
import time
import re
import os
from datetime import datetime
from modules.recon import run_recon
from modules.web_vuln import run_web_vuln
from modules.brute_force import run_brute_force
from modules.flag_finder import run_flag_finder
from modules.file_scanner import run_file_scanner
from modules.hint_decoder import run_hint_decoder

# Initialize Colorama for colored output
colorama.init()

# Theme configuration (customizable: Hacker Green, Cyber Blue, Red Team)
theme = "Red Team"  # Changed to Red Team for that hacker flair
THEMES = {
    "Hacker Green": {"menu": Fore.CYAN, "success": Fore.GREEN, "error": Fore.RED, "input": Fore.YELLOW},
    "Cyber Blue": {"menu": Fore.BLUE, "success": Fore.CYAN, "error": Fore.MAGENTA, "input": Fore.WHITE},
    "Red Team": {"menu": Fore.RED, "success": Fore.YELLOW, "error": Fore.WHITE, "input": Fore.CYAN}
}
colors = THEMES.get(theme, THEMES["Hacker Green"])

# Global variables
global_mode = "Normal"
stealth_mode = False
config = {}
results = []

def log_action(message):
    """Log actions/errors to ctf_log.txt"""
    try:
        with open("data/ctf_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except Exception as e:
        print(f"{colors['error']}[-] Error logging: {e}{Style.RESET_ALL}")

def save_results(task, result):
    """Save task result to ctf_results.json"""
    try:
        results.append({"task": task, "result": result, "timestamp": str(datetime.now())})
        with open("data/ctf_results.json", "w") as f:
            json.dump(results, f, indent=2)
        log_action(f"Saved result for {task}")
    except Exception as e:
        print(f"{colors['error']}[-] Error saving results: {e}{Style.RESET_ALL}")
        log_action(f"Error saving results: {e}")

def load_results():
    """Load results from ctf_results.json"""
    try:
        with open("data/ctf_results.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("data/ctf_results.json", "w") as f:
            json.dump([], f)
        log_action("Created empty ctf_results.json")
        return []
    except Exception as e:
        print(f"{colors['error']}[-] Error loading results: {e}{Style.RESET_ALL}")
        log_action(f"Error loading results: {e}")
        return []

def validate_ip(ip):
    """Validate IP address format"""
    ip = ip.strip()
    ip_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(ip_pattern, ip))

def validate_url(url):
    """Validate URL format"""
    url = url.strip()
    url_pattern = r"^(http|https)://[a-zA-Z0-9.-]+(:[0-9]+)?(/[a-zA-Z0-9._/-]*)?$"
    return bool(re.match(url_pattern, url))

def print_menu():
    """Print stylized menu with ASCII art"""
    print(f"{colors['menu']}")
    print("======================================")
    print("     CTFBlitz: Pwn the Flags! 😎     ")
    print("======================================")
    print("0. Quick Help")
    print("1. Quick Recon")
    print("2. Web Vuln Deep Dive")
    print("3. Mega Brute-Forcer")
    print("4. Flag Finder")
    print("5. Hidden File Scanner")
    print("6. Hint Decoder")
    print(f"7. Toggle Mode: [{global_mode}]")
    print("8. View Results Summary")
    print("9. Manage Config Profiles")
    print(f"10. Toggle Stealth Mode: [{'On' if stealth_mode else 'Off'}]")
    print(f"11. Exit")
    print(f"{Style.RESET_ALL}")

def main():
    global global_mode, stealth_mode, config, results
    results = load_results()
    log_action("Started CTFBlitz")

    while True:
        print_menu()
        choice = input(f"{colors['input']}Choose (0-11): {Style.RESET_ALL}").strip()

        if choice == "0":
            print(f"{colors['menu']}=== CTFBlitz Quick Help ===")
            print("[0] Quick Help: You're here! Shows this guide.")
            print("[1] Quick Recon: Scans ports like a ninja. Normal: Top 100 or custom range (e.g., 80-100). Advanced: All ports, vulns (e.g., CVE-2021-41773).")
            print("[2] Web Vuln Deep Dive: Hunts web bugs like Burp Suite. Normal: Headers, 10 paths. Advanced: Crawls links, 100+ paths, params (e.g., id=1 for IDOR).")
            print("[3] Mega Brute-Forcer: Cracks logins like a boss. Normal: 50 CTF creds, 1000 usernames. Advanced: 10,000 passwords (rockyou_small.txt).")
            print("[4] Flag Finder: Snipes flags (e.g., flag{1234}). Normal: One file/URL, suggests formats (flag{.*}, HTB{.*}). Advanced: Crawls HTML/JS.")
            print("[5] Hidden File Scanner: Finds secret files like /flag.txt. Normal: 10 files (e.g., robots.txt). Advanced: 100+ files, tries .bak, .txt, .zip.")
            print("[6] Hint Decoder: Cracks CTF hints. Normal: Base64, hex. Advanced: ROT13, URL, Caesar.")
            print("[7] Toggle Mode: Switch Normal (fast) or Advanced (deep) for all tools.")
            print("[8] View Results: Shows your pwnage (ports, flags, creds).")
            print("[9] Manage Config: Save/load your CTF setups (IPs, wordlists).")
            print("[10] Toggle Stealth: Random delays (0.5-2s) to stay sneaky.")
            print("[11] Exit: Saves results, dips out. Pwn those flags, boss! 😎")
            print(f"{Style.RESET_ALL}")
            log_action("Displayed Quick Help")
        elif choice == "1":
            ip = config.get("recon_ip", input(f"{colors['input']}Enter IP: {Style.RESET_ALL}")).strip()
            if not validate_ip(ip):
                print(f"{colors['error']}[-] Invalid IP, try again!{Style.RESET_ALL}")
                log_action(f"Invalid IP: {ip}")
                continue
            config["recon_ip"] = ip
            result = run_recon(ip, global_mode, stealth_mode, colors)
            save_results("Quick Recon", result)
            print(f"{colors['success']}{result}{Style.RESET_ALL}")
        elif choice == "2":
            url = config.get("web_url", input(f"{colors['input']}Enter URL (e.g., http://10.10.10.10): {Style.RESET_ALL}")).strip()
            if not validate_url(url):
                print(f"{colors['error']}[-] Invalid URL, try again!{Style.RESET_ALL}")
                log_action(f"Invalid URL: {url}")
                continue
            config["web_url"] = url
            result = run_web_vuln(url, global_mode, stealth_mode, colors)
            save_results("Web Vuln Deep Dive", result)
            print(f"{colors['success']}{result}{Style.RESET_ALL}")
        elif choice == "3":
            url = config.get("brute_url", input(f"{colors['input']}Enter login URL: {Style.RESET_ALL}")).strip()
            if not validate_url(url):
                print(f"{colors['error']}[-] Invalid URL, try again!{Style.RESET_ALL}")
                log_action(f"Invalid URL: {url}")
                continue
            username_field = config.get("username_field", input(f"{colors['input']}Enter username field (e.g., username): {Style.RESET_ALL}")).strip()
            password_field = config.get("password_field", input(f"{colors['input']}Enter password field (e.g., password): {Style.RESET_ALL}")).strip()
            username_file = config.get("username_file", input(f"{colors['input']}Enter username file (e.g., data/usernames.txt): {Style.RESET_ALL}")).strip()
            password_file = config.get("password_file", "data/ctf_creds.txt" if global_mode == "Normal" else input(f"{colors['input']}Enter password file (e.g., data/rockyou_small.txt): {Style.RESET_ALL}")).strip()
            if not os.path.exists(username_file):
                print(f"{colors['error']}[-] Username file not found!{Style.RESET_ALL}")
                log_action(f"Username file not found: {username_file}")
                continue
            if not os.path.exists(password_file):
                print(f"{colors['error']}[-] Password file not found!{Style.RESET_ALL}")
                log_action(f"Password file not found: {password_file}")
                continue
            config.update({"brute_url": url, "username_field": username_field, "password_field": password_field, "username_file": username_file, "password_file": password_file})
            result = run_brute_force(url, username_field, password_field, username_file, password_file, global_mode, stealth_mode, colors)
            save_results("Mega Brute-Forcer", result)
            print(f"{colors['success']}{result}{Style.RESET_ALL}")
        elif choice == "4":
            target = config.get("flag_target", input(f"{colors['input']}Enter file/URL to search: {Style.RESET_ALL}")).strip()
            if not (validate_url(target) or target.startswith("data/")):
                print(f"{colors['error']}[-] Invalid file/URL, try again!{Style.RESET_ALL}")
                log_action(f"Invalid file/URL: {target}")
                continue
            config["flag_target"] = target
            result = run_flag_finder(target, global_mode, stealth_mode, colors)
            save_results("Flag Finder", result)
            print(f"{colors['success']}{result}{Style.RESET_ALL}")
        elif choice == "5":
            url = config.get("file_url", input(f"{colors['input']}Enter URL (e.g., http://10.10.10.10): {Style.RESET_ALL}")).strip()
            if not validate_url(url):
                print(f"{colors['error']}[-] Invalid URL, try again!{Style.RESET_ALL}")
                log_action(f"Invalid URL: {url}")
                continue
            config["file_url"] = url
            result = run_file_scanner(url, global_mode, stealth_mode, colors)
            save_results("Hidden File Scanner", result)
            print(f"{colors['success']}{result}{Style.RESET_ALL}")
        elif choice == "6":
            text = config.get("decode_text", input(f"{colors['input']}Enter text to decode: {Style.RESET_ALL}")).strip()
            config["decode_text"] = text
            result = run_hint_decoder(text, global_mode, stealth_mode, colors)
            save_results("Hint Decoder", result)
            print(f"{colors['success']}{result}{Style.RESET_ALL}")
        elif choice == "7":
            global_mode = "Advanced" if global_mode == "Normal" else "Normal"
            print(f"{colors['success']}Mode: {global_mode}—ready to pwn!{Style.RESET_ALL}")
            log_action(f"Toggled mode to {global_mode}")
        elif choice == "8":
            results = load_results()
            if not results:
                print(f"{colors['error']}[-] No results yet! Go pwn some flags!{Style.RESET_ALL}")
                log_action("No results in dashboard")
            else:
                print(f"{colors['menu']}=== CTFBlitz Results Dashboard ===")
                for r in results:
                    print(f"{colors['success']}[+] {r['task']} ({r['timestamp']}): {r['result']}{Style.RESET_ALL}")
                log_action("Displayed results dashboard")
        elif choice == "9":
            sub_choice = input(f"{colors['input']}1. Save Config 2. Load Config 3. List Configs: {Style.RESET_ALL}").strip()
            try:
                if sub_choice == "1":
                    name = input(f"{colors['input']}Config name: {Style.RESET_ALL}").strip()
                    if not name:
                        print(f"{colors['error']}[-] Config name cannot be empty!{Style.RESET_ALL}")
                        log_action("Empty config name attempted")
                        continue
                    with open("data/config.json", "w") as f:
                        json.dump({name: config}, f, indent=2)
                    print(f"{colors['success']}[+] Saved config '{name}'—ready for next pwn!{Style.RESET_ALL}")
                    log_action(f"Saved config '{name}'")
                elif sub_choice == "2":
                    name = input(f"{colors['input']}Config name: {Style.RESET_ALL}").strip()
                    with open("data/config.json") as f:
                        configs = json.load(f)
                        if name not in configs:
                            print(f"{colors['error']}[-] Config '{name}' not found!{Style.RESET_ALL}")
                            log_action(f"Config not found: {name}")
                            continue
                        config = configs.get(name, {})
                    print(f"{colors['success']}[+] Loaded config '{name}'—let's hack!{Style.RESET_ALL}")
                    log_action(f"Loaded config '{name}'")
                elif sub_choice == "3":
                    try:
                        with open("data/config.json") as f:
                            configs = json.load(f)
                        print(f"{colors['menu']}Configs: {', '.join(configs.keys()) or 'None'}{Style.RESET_ALL}")
                        log_action("Listed configs")
                    except FileNotFoundError:
                        print(f"{colors['error']}[-] No configs found!{Style.RESET_ALL}")
                        log_action("No configs found")
            except FileNotFoundError:
                print(f"{colors['error']}[-] No configs found! Save one first!{Style.RESET_ALL}")
                log_action("No config file found")
            except Exception as e:
                print(f"{colors['error']}[-] Error managing configs: {e}{Style.RESET_ALL}")
                log_action(f"Config error: {e}")
        elif choice == "10":
            stealth_mode = not stealth_mode
            print(f"{colors['success']}Stealth Mode: {'On' if stealth_mode else 'Off'}—sneaky vibes, boss! 😎{Style.RESET_ALL}")
            log_action(f"Toggled Stealth Mode to {'On' if stealth_mode else 'Off'}")
        elif choice == "11":
            print(f"{colors['menu']}CTFBlitz out—pwn those flags, boss! 😎{Style.RESET_ALL}")
            log_action("Exiting CTFBlitz")
            break
        else:
            print(f"{colors['error']}[-] Invalid choice, try 0-11!{Style.RESET_ALL}")
            log_action(f"Invalid menu choice: {choice}")

if __name__ == "__main__":
    main()