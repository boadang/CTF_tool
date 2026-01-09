import requests

def main():
    method = input("Method (GET/POST): ").upper()
    url = input("URL: ")

    # Headers
    headers = {}
    print("Nhập headers (Header: value), Enter trống để kết thúc:")
    while True:
        line = input()
        if line == "":
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()

    # Cookies
    cookies = {}
    print("Nhập cookies (key=value), Enter trống để kết thúc:")
    while True:
        line = input()
        if line == "":
            break
        key, value = line.split("=", 1)
        cookies[key.strip()] = value.strip()

    # Send request
    if method == "GET":
        r = requests.get(url, headers=headers, cookies=cookies)
    elif method == "POST":
        r = requests.post(url, headers=headers, cookies=cookies)
    else:
        print("Method không hỗ trợ")
        return

    # Output
    print("\n===== RESPONSE =====")
    print("Status code:", r.status_code)
    print("Response length:", len(r.text))
    print("First 100 chars:")
    print(r.text[:100])

if __name__ == "__main__":
    main()
