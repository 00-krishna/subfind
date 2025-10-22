import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_subdomains(wordlist_file):
    try:
        with open(wordlist_file, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Wordlist file '{wordlist_file}' not found.")
        return []

def resolve_domain(subdomain, domain):
    full_domain = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return (full_domain, ip)
    except socket.gaierror:
        return None

def main():
    domain = input("Enter the domain to scan (e.g., example.com): ").strip()
    wordlist_file = "list.txt"  # Update with your actual wordlist path
    subdomains = load_subdomains(wordlist_file)

    if not subdomains:
        print("[!] No subdomains loaded. Exiting.")
        return

    print(f"[+] Loaded {len(subdomains)} potential subdomains.")
    print("[+] Starting scan...\n")

    found = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(resolve_domain, sub, domain): sub for sub in subdomains}
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                found.append(result)
                print(f"[{i}] [FOUND] {result[0]} => {result[1]}")

    print("\n[+] Scan completed.")
    print(f"[+] Total active subdomains found: {len(found)}")

    for sub, ip in found:
        print(f"{sub} => {ip}")

if __name__ == "__main__":
    main()
