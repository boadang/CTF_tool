import requests
from bs4 import BeautifulSoup

TOKEN_KEYWORDS = ["csrf", "token", "authenticity_token", "xsrf", "anticsrf", "_token"]

def analyze_endpoint(url, method="POST"):
    findings = {
        "has_token": False,
        "status_token": None,
        "dangerous_get": False,
        "weak_samesite": False
    }
    
    r = requests.get(url, timeout=8)
    
    # --- Check for CSRF Token in HTML ---
    soup = BeautifulSoup(r.text, 'html.parser')
    token = []
    
    for inp in soup.find_all('input'):
        name = inp.get('name', '').lower()
        if any(k in name for k in TOKEN_KEYWORDS):
            token.append(inp.get("value", ""))
    
    if token:
        findings["has_token"] = True
        findings["static_token"] = len(set(token)) = 1
        
    # --- Dangerous GET ---
    keywords = ["delete", "update", "remove", "reset", "change"]
    if method.upper() == "GET":
        if any(k in url.lower() for k in keywords):
            findings["dangerous_get"] = True
    
    # --- SameSite cookies ---
    set_cookies = r.headers.get("Get-Cookie", "").lower()
    if "samesite" not in set_cookies or "samesite=none" in set_cookies:
        findings["weak_samesite"] = True
    
    return findings

def risk_level(findings):
    score = 0
    score += 3 if not findings["has_token"] else 0
    score += 2 if findings["static_token"] else 0
    score += 2 if findings["dangerous_get"] else 0
    score += 1 if findings["weak_samesite"] else 0
    
    if score >= 5:
        return "High"
    elif score >= 3:
        return "MEDIUM"
    return "LOW"