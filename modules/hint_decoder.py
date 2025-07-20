import base64
import colorama
from colorama import Fore, Style
import urllib.parse
import re
from datetime import datetime

def log_action(message):
    """Log actions/errors to ctf_log.txt"""
    try:
        with open("data/ctf_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except Exception as e:
        print(f"{Fore.RED}[-] Error logging: {e}{Style.RESET_ALL}")

def run_hint_decoder(text, mode, stealth_mode, colors):
    """Decode CTF hints like a crypto pro"""
    try:
        result = []
        print(f"{colors['success']}[+] Decoding {text}... Cracking the code!{Style.RESET_ALL}")
        log_action(f"Starting decode on {text}")
        # Base64
        try:
            decoded = base64.b64decode(text).decode()
            result.append(f"Pwned! Decoded: {decoded} (base64)")
        except:
            result.append("Not base64")
        # Hex
        try:
            decoded = bytes.fromhex(text).decode()
            result.append(f"Pwned! Decoded: {decoded} (hex)")
        except:
            result.append("Not hex")
        if mode == "Advanced":
            # ROT13
            rot13_trans = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 
                                       "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm")
            decoded = text.translate(rot13_trans)
            result.append(f"Decoded: {decoded} (ROT13)")
            # URL decode
            decoded = urllib.parse.unquote(text)
            result.append(f"Decoded: {decoded} (URL)")
            # Caesar cipher
            for shift in range(1, 26):
                caesar_trans = str.maketrans("abcdefghijklmnopqrstuvwxyz", 
                                            "abcdefghijklmnopqrstuvwxyz"[shift:] + "abcdefghijklmnopqrstuvwxyz"[:shift])
                decoded = text.lower().translate(caesar_trans)
                if "flag" in decoded.lower():
                    result.append(f"Pwned! Decoded: {decoded} (Caesar shift {shift})")
        log_action(f"Decode completed on {text}")
        return "\n".join(result) or f"{colors['error']}[-] No decodings found! Try another hint!{Style.RESET_ALL}"
    except Exception as e:
        log_action(f"Decoder error: {e}")
        return f"{colors['error']}[-] Decoder error: {e}{Style.RESET_ALL}"