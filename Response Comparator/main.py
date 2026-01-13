# Response Comparator

# Purpose: turn ambiguous differences into automatic TRUE/ FALSE conclusions

# Step 1: Entering the URL, Param need to fuzz, Payload TRUE, Payload FALSE, Keyword (options)
# Step 2: Parsing URL to partials
# Step 3: Assigning the payload true and false onto URL to create the new URL
# Step 4: Based on the keyword exiting condition, Checking the response
# Step 5: Saving the length and status of both response true and false

# parse_qs: a method that parses a query string into a dictionary, access the components via keys like parses['param']
# urlencode: a method that parses a dictionary into a query string
# urlparse: a method that breaks down a URL into its components like schema, netloc, path, params, query, fragment
#          . So that it really helps to manipulate different parts of a URL easily
#          . Access the its components via attributes like .scheme, .netloc,...
# urlunparse: a method that builds back a URL from its components

# Why we need LENGTH_THRESHOLD variable?
# Because sometimes the length difference between TRUE and FALSE responses is too small to be conclusive.
# By setting a threshold, we can filter out minor variations that may not be significant,
# thus reducing false positives in our comparison results.
# If the length difference is smaller than this threshold, we consider the length comparison inconclusive.
# On the other hand, if this is greater than this threshold, we can confidently say that the response with the greater length is likely the TRUE response.

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from enum import Enum

TIMEOUT = 8
LENGTH_THRESHOLD = 30


class CompareResult(Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"


def build_url(url, param, payload):
    """
    Replace param value with payload and rebuild URL
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    qs[param] = [payload]

    new_query = urlencode(qs, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def send(url):
    """
    Send request and normalize response info
    """
    try:
        r = requests.get(url, timeout=TIMEOUT, allow_redirects=False)
        return {
            "status": r.status_code,
            "length": len(r.text),
            "text": r.text
        }
    except requests.RequestException as e:
        return {
            "status": None,
            "length": 0,
            "text": "",
            "error": str(e)
        }


def compare(true_resp, false_resp, keyword=None):
    """
    Compare TRUE vs FALSE responses
    Return: TRUE / FALSE / UNKNOWN
    """

    # 1. Status code class comparison (strongest)
    if true_resp["status"] != false_resp["status"]:
        if true_resp["status"] and false_resp["status"]:
            if true_resp["status"] < false_resp["status"]:
                return CompareResult.TRUE
            else:
                return CompareResult.FALSE

    # 2. Keyword-based comparison
    if keyword:
        in_true = keyword in true_resp["text"]
        in_false = keyword in false_resp["text"]

        if in_true and not in_false:
            return CompareResult.TRUE
        if in_false and not in_true:
            return CompareResult.FALSE

    # 3. Length-based comparison
    diff = abs(true_resp["length"] - false_resp["length"])
    if diff > LENGTH_THRESHOLD:
        if true_resp["length"] > false_resp["length"]:
            return CompareResult.TRUE
        else:
            return CompareResult.FALSE

    return CompareResult.UNKNOWN


def main():
    url = input("Enter URL: ").strip()
    param = input("Enter param to fuzz: ").strip()
    payload_true = input("Enter payload TRUE: ").strip()
    payload_false = input("Enter payload FALSE: ").strip()
    keyword = input("Enter keyword (optional): ").strip()

    keyword = keyword if keyword else None

    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    if param not in qs:
        print(f"[!] Param '{param}' not found in URL")
        return

    url_true = build_url(url, param, payload_true)
    url_false = build_url(url, param, payload_false)

    print("[*] Sending TRUE payload...")
    true_resp = send(url_true)

    print("[*] Sending FALSE payload...")
    false_resp = send(url_false)

    result = compare(true_resp, false_resp, keyword)

    print("\n=== RESULT ===")
    print(f"TRUE  -> status: {true_resp['status']}, length: {true_resp['length']}")
    print(f"FALSE -> status: {false_resp['status']}, length: {false_resp['length']}")
    print(f"COMPARE RESULT: {result.value}")


if __name__ == "__main__":
    main()
