#!/usr/bin/env python3

__version__ = 'v1.0.0'

try:
    import sys
    from colorama import Fore, Style
    import atexit
    import argparse
    import random
    import time
    import json
    import re
    import requests
    from bs4 import BeautifulSoup
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    import os  
except KeyboardInterrupt:
    print('[!] Exiting.')
    sys.exit()
except Exception as e:
    print(f'[!] Missing requirements. Please ensure you have the necessary packages installed: {e}')
    sys.exit()

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def vibrating_banner():
    """Display a vibrating phone icon banner."""
    phone_icon = r"""
        📱
    """
    
    bold_fonehunt = "\033[1mFoneNinja\033[0m"
    
    for _ in range(3):  
        clear_terminal()
        print(f"\n{phone_icon}")
        print(f"\n{bold_fonehunt} is loading...")
        time.sleep(0.1)  

def banner():
    """Display the main banner for the tool."""
    print(r"""
    📱📱📱📱🥶🥶🥶🥶🥶🥶🥶🥶📱📱📱📱📱📱📱📱📱📱📱
    📱📱📱📱📱📱🥶🥶🥶🥶🥶🥶🥶🥶📱📱📱📱📱📱📱📱📱
    📱📱📱📱📱📱📱📱🥶🥶🥶🥶🥶🥶🥶🥶📱📱📱📱📱📱📱
                                                                                         
                      FoneNinja
                    Version: {}
                    Coded by celestialsapien
""".format(__version__))

# Call the vibrating banner function
vibrating_banner()
banner()

if sys.version_info[0] < 3:
    print("\033[1m\033[93m(!) Please run the tool using Python 3" + Style.RESET_ALL)
    sys.exit()

# Argument parser setup
parser = argparse.ArgumentParser(description="Advanced information gathering tool for phone numbers (https://github.com/hackosapiens/FoneNinja) version {}".format(__version__), usage='%(prog)s -n [options]')
parser.add_argument('-n', '--number', metavar='number', type=str, help='The phone number to scan (E164 or international format)', required=True)
parser.add_argument('-i', '--input', metavar="input_file", type=argparse.FileType('r'), help='Phone number list to scan (one per line)')
parser.add_argument('-o', '--output', metavar="output_file", type=argparse.FileType('w'), help='Output to save scan results')
parser.add_argument('--osint', action='store_true', help='Use OSINT reconnaissance')
parser.add_argument('--proxy', type=str, help='Proxy server to use for requests (e.g., http://127.0.0.1:8080)')
args = parser.parse_args()

def resetColors():
    """Reset text colors at exit."""
    if not args.output:
        print(Style.RESET_ALL)

atexit.register(resetColors)

# Disable SSL warnings for requests
requests.packages.urllib3.disable_warnings()

# Proxy setup for privacy features
proxies = {}
if args.proxy:
    proxies = {
        "http": args.proxy,
        "https": args.proxy,
    }

def search(req):
    """Perform a Google search with the specified query."""
    chosenUserAgent = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
    ])
    
    headers = {
        'User-Agent': chosenUserAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        URL = f'https://www.google.com/search?q={req}'
        response = requests.get(URL, headers=headers, proxies=proxies)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all('div', class_='g')
            links = [result.find('a')['href'] for result in results if result.find('a')]
            return links
        else:
            print(f"[!] Error fetching search results: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return []

def formatNumber(input_number):
    """Format the input number to E164 format."""
    return re.sub(r"(?:\+)?(?:[^[0-9]*)", "", input_number)

def localScan(input_number):
    """Scan a local phone number for details."""
    formatted_number = "+" + formatNumber(input_number)
    print(f"[DEBUG] Formatted Number: {formatted_number}")  # Debugging line
    
    try:
        phone_number_object = phonenumbers.parse(formatted_number, None)
        
        if not phonenumbers.is_valid_number(phone_number_object):
            print(f"[!] Invalid phone number: {formatted_number}")
            return
        
        # Continue with processing...
        
    except Exception as e:
        print(f"[!] Error processing number: {e}")

def osintScan():
    """Perform OSINT reconnaissance on the phone number."""
    if args.osint:
        try:
            with open('osint/individuals.json') as f:
                dorks = json.load(f)  # Load OSINT dorks from a JSON file

            for dork in dorks:
                request_url = f"{dork['request']} {args.number}"
                links = search(request_url)
                for link in links:
                    print(f"[OSINT Link Found]: {link}")

        except FileNotFoundError:
            print("[!] OSINT file 'individuals.json' not found. Please ensure it exists in the 'osint' directory.")
        except json.JSONDecodeError:
            print("[!] Error decoding JSON from OSINT file.")
        
if __name__ == "__main__":
    
     if args.number:
         localScan(args.number)
     
     if args.osint:
         osintScan()        
