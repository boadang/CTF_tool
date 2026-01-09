import string
import requests

def wordlist():
    print("=========WORDLISTS OPTIONS===========")
    print("1.Alphabet (a-z, A-Z)")
    print("2.Numbers (1-n)")
    result = {}

    opt = input("Enter your options")
    match(opt):
        case 1:
            result = list(string.ascii_letters)
        case 2:
            result = list(string.digits)
    return result

def match_status(r):
    if 200 <= r.status_code < 300:
        result = "SUCCESS"
        return result
    elif 300 <= r.status_code < 400:
        result = "REDIRECT"
    elif 400 <= r.status_code < 500:
        result = "CLIENT_ERROR"
    elif 500 <= r.status_code < 600:
        result = "SERVER_ERROR"

def main():
    url = input("Enter your URL:").strip()
    input_param = input("Enter the name you want to fuzz:").strip()
    w_list = wordlist()

    result = {}
    status = {}

    for char in w_list:
        param = input_param.split("=",1)
        count = 1
        for char_p in param:
            if(char_p == char):
                result.append(param)
            count += 1

    r = requests.post(url)
    return

if __name__ == "__main__":
    main()
