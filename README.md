CTFBlitz: Elite CTF Toolkit
CTFBlitz is a Python-based, menu-driven toolkit for crushing Capture The Flag (CTF) challenges on TryHackMe and HackTheBox. With dual Normal/Advanced modes, Stealth Mode with random delays, customizable themes, and CTF-focused tools, it’s your ultimate weapon for sniping flags and flexing on GitHub!
Features

Quick Recon: Scans ports like Nmap. Normal: Top 100 or custom range (e.g., 80-100, ~5s). Advanced: All ports, vulns (e.g., CVE-2021-41773, ~1–2m).
Web Vuln Deep Dive: Hunts web bugs like Burp Suite. Normal: Headers, 10 paths (10s). Advanced: Crawls links, 100+ paths, params (1–2m).
Mega Brute-Forcer: Cracks logins. Normal: 50 CTF creds, 1000 usernames (~5–10s). Advanced: 10,000 passwords (rockyou_small.txt, ~1–2m).
Flag Finder: Snipes flags (e.g., flag{1234}). Normal: One file/URL, suggests formats (flag{.}, HTB{.}, 5s). Advanced: Crawls HTML/JS (30s).
Hidden File Scanner: Finds secret files (e.g., /flag.txt). Normal: 10 files (5–10s). Advanced: 100+ files, tries .bak, .txt, .zip (30–60s).
Hint Decoder: Cracks hints. Normal: Base64, hex (2–5s). Advanced: ROT13, URL, Caesar (5–10s).
Toggle Mode: Switch Normal (fast) or Advanced (deep) globally.
View Results: Session dashboard of findings (ports, flags, creds).
Manage Config Profiles: Save/load CTF setups (IPs, wordlists).
Stealth Mode: Random delays (0.5–2s) to avoid detection.
Quick Help: Hacker-style guide for all features.
Themes: Customize colors (Hacker Green, Cyber Blue, Red Team).

Setup

Clone the repo: git clone <your-repo-url>
Install dependencies: pip install -r requirements.txt
Copy common.txt from dirb: cp /usr/share/dirb/wordlists/common.txt data/
Download usernames.txt (1000 usernames, e.g., from seclists on GitHub) to data/.
Create rockyou_small.txt: head -n 10000 /usr/share/wordlists/rockyou.txt > data/rockyou_small.txt
Ensure data/ is writable for ctf_results.json, config.json, ctf_log.txt.
Run with sudo for Advanced Recon (uses -O): sudo python ctfblitz.py

Usage

Run python ctfblitz.py to start the menu.
Choose 0–11 for features, toggle modes, or view help.
Customize theme in ctfblitz.py (set theme to "Hacker Green", "Cyber Blue", or "Red Team").
Results save to data/ctf_results.json, logs to data/ctf_log.txt.
Adjust "login failed" check in brute_force.py for specific CTF login pages.

Notes

Tested on Kali Linux with Python 3.9+.
Use on TryHackMe/HackTheBox VMs only.
Download usernames.txt from seclists (GitHub) and common.txt from dirb.
Create rockyou_small.txt for faster Advanced brute-forcing.
Check ctf_log.txt for debugging.

Pwn those flags, boss! 😎