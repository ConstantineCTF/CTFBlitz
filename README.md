# CTFBlitz: Elite CTF Toolkit 😎

**CTFBlitz** is a Python-based, menu-driven toolkit designed to *crush* Capture The Flag (CTF) challenges on **TryHackMe** and **HackTheBox**. With dual **Normal/Advanced** modes, **Stealth Mode** with random delays, customizable themes, and CTF-focused tools, it’s your ultimate weapon for sniping flags and flexing on GitHub for bug bounties or certifications like eJPT/OSCP!

## Features

- **Quick Recon**: Scans ports like a pro with `nmap`.  
  - *Normal*: Top 100 ports or custom range (e.g., `80-100`, ~5s).  
  - *Advanced*: All ports, services, OS, vulns (e.g., CVE-2021-41773, ~1–2m).
- **Web Vuln Deep Dive**: Hunts web bugs like Burp Suite.  
  - *Normal*: Checks headers, 10 paths (~10s).  
  - *Advanced*: Crawls links, 100+ paths, params (e.g., `id=1` for IDOR, ~1–2m).
- **Mega Brute-Forcer**: Cracks logins like a red team boss.  
  - *Normal*: 50 CTF creds (`data/ctf_creds.txt`), 1000 usernames (`data/usernames.txt`, ~5–10s).  
  - *Advanced*: 10,000 passwords (`data/rockyou_small.txt`, ~1–2m).
- **Flag Finder**: Snipes flags (e.g., `flag{1234}`).  
  - *Normal*: Scans one file/URL, suggests formats (`flag{.*}`, `HTB{.*}`, ~5s).  
  - *Advanced*: Crawls HTML/JS/comments (~30s).
- **Hidden File Scanner**: Finds secret files (e.g., `/flag.txt`).  
  - *Normal*: 10 files (e.g., `robots.txt`, ~5–10s).  
  - *Advanced*: 100+ files (`data/common.txt`), tries `.bak`, `.txt`, `.zip` (~30–60s).
- **Hint Decoder**: Cracks CTF hints like a crypto pro.  
  - *Normal*: Base64, hex (~2–5s).  
  - *Advanced*: ROT13, URL, Caesar (~5–10s).
- **Toggle Mode**: Switch between **Normal** (fast) and **Advanced** (deep) globally.
- **View Results**: Session dashboard of findings (ports, flags, creds) in `data/ctf_results.json`.
- **Manage Config Profiles**: Save/load CTF setups (IPs, URLs, wordlists) in `data/config.json`.
- **Stealth Mode**: Random delays (0.5–2s) to stay sneaky.
- **Quick Help**: Hacker-style guide for all features.
- **Themes**: Customize colors (**Hacker Green**, **Cyber Blue**, **Red Team**) in `ctfblitz.py`.

## Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/ConstantineCTF/CTFBlitz.git
   cd CTFBlitz
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare data files**:
   - Copy `common.txt` (from `dirb` wordlists):
     - **Kali Linux**: `cp /usr/share/dirb/wordlists/common.txt data/`
     - **Windows**: Download from [dirb GitHub](https://github.com/v0re/dirb/blob/master/wordlists/common.txt) and save to `data/`.
   - Download `usernames.txt` (1000 usernames):
     - Get from [SecLists/Usernames](https://github.com/danielmiessler/SecLists/tree/master/Usernames) and save to `data/`.
   - Create `rockyou_small.txt` (10,000 passwords):
     - **Kali Linux**: `head -n 10000 /usr/share/wordlists/rockyou.txt > data/rockyou_small.txt`
     - **Windows**: Download `rockyou.txt` (e.g., from [SecLists/Passwords](https://github.com/danielmiessler/SecLists/tree/master/Passwords)), then:
       ```bash
       head -n 10000 /path/to/rockyou.txt > data/rockyou_small.txt
       ```
       Replace `/path/to/rockyou.txt` with its location (e.g., `/c/Users/YourName/Downloads/rockyou.txt`).
   - Ensure `data/ctf_creds.txt` exists (included in repo).
4. **Ensure `data/` is writable**:
   ```bash
   chmod -R u+w data/
   ```
5. **Run with sudo for Advanced Recon** (uses `-O` in `nmap`):
   - **Kali Linux**: `sudo python ctfblitz.py`
   - **Windows**: Run in an elevated terminal (if `nmap` is installed).

## Usage

- Run `python ctfblitz.py` to launch the menu.
- Choose options 0–11 for features, toggle modes, or view help.
- Customize the theme in `ctfblitz.py` (set `theme` to `"Hacker Green"`, `"Cyber Blue"`, or `"Red Team"`).
- Results save to `data/ctf_results.json`, logs to `data/ctf_log.txt`.
- For specific CTF login pages, adjust the `"login failed"` check in `modules/brute_force.py`.

## Notes

- Tested on **Kali Linux** (Python 3.9+) and **Windows** (with Git Bash and Python).
- Use only on **TryHackMe** or **HackTheBox** VMs to stay legal.
- Download `usernames.txt` from [SecLists](https://github.com/danielmiessler/SecLists) and `common.txt` from [dirb](https://github.com/v0re/dirb).
- Create `rockyou_small.txt` for faster Advanced brute-forcing.
- Check `data/ctf_log.txt` for debugging.

**Pwn those flags, boss!** 😎