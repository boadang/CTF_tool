import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Flow tools:
# B1: get wordlist
# B2: Get input from user including URL, param which you want to fuzz, wordlist choice
# B3: Parsing URL to field partials
# B4: Finding (key (maybe param which user entered), value) to add into dict
# B5: Based on the dict created and word list, replacing value by the char or number in word list alternatively.
#     Merge all of partials become new URL, then, post it to check response (observe this message response to diffirent the change)    

def get_wordlist(choice):
    if choice == "1":  # number
        n = int(input("Max number: "))
        return [str(i) for i in range(1, n + 1)]
    elif choice == "2":  # alphabet
        return [chr(c) for c in range(ord('a'), ord('z') + 1)]
    elif choice == "3":  # special chars
        return ["'", "\"", "--", "#", "/*", "%00"]
    else:
        return []

def main():
    url = input("URL: ").strip()
    param_to_fuzz = input("Param to fuzz: ").strip()

    print("""
Choose wordlist:
1. Number (1 → n)
2. Alphabet (a-z)
3. Special characters
""")
    choice = input("Your choice: ").strip()
    wordlist = get_wordlist(choice)

    # Parse URL
    parsed = urlparse(url) # urlparse: divide URL to fields (scheme, netloc, path, query, fragment)
    query_dict = parse_qs(parsed.query) # parse_qs: convert query string to dict key-value, such as id=123&name=bin -> "id": ["123"],...

    if param_to_fuzz not in query_dict:
        print(f"[!] Param '{param_to_fuzz}' not found in URL")
        return

    original_value = query_dict[param_to_fuzz][0]

    print("\nPayload | Status | Length")
    print("-" * 30)

    for payload in wordlist:
        # Replace only target param
        query_dict[param_to_fuzz] = [payload]

        new_query = urlencode(query_dict, doseq=True) # urlencode: Convert dict to string, doseq=True: allow list convert correctly encode
        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        )) # merge the URL completely parts from the parts which was parsed 

        r = requests.get(new_url)

        print(f"{payload} | {r.status_code} | {len(r.text)}")

    print("\nDone.")

if __name__ == "__main__":
    main()
