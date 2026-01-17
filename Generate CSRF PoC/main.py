# main.py
from anlyze import analyze_endpoint, risk_level
from generator import generate_csrf_poc

def main():
    url = input("Target URL: ").strip()
    method = input("Method (GET/POST): ").strip().upper()

    params = {}
    print("Enter params (key=value), empty line to stop:")
    while True:
        line = input("> ").strip()
        if not line:
            break
        k, v = line.split("=", 1)
        params[k] = v

    findings = analyze_endpoint(url, method)
    risk = risk_level(findings)

    print("\n[+] Analysis result:")
    for k, v in findings.items():
        print(f" - {k}: {v}")
    print(f"[+] CSRF Risk Level: {risk}")

    if risk in ("HIGH", "MEDIUM"):
        html = generate_csrf_poc(url, method, params)
        with open("csrf_poc.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("[+] PoC generated: csrf_poc.html")
    else:
        print("[!] Risk low – PoC not generated")

if __name__ == "__main__":
    main()
