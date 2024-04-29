import requests
import tqdm
import time

path = []
with open('direction.txt', 'r') as f:
    path = [line.strip() for line in f]

url = 'http://blindmazerevenge.challs.open.ecsc2024.it/maze?direction='
print(path)

with requests.Session() as session:
    response = session.get(url + 'start')
    for value in tqdm.tqdm(path):
        response = session.get(url + value)
        if 'Last Move: FAILED because the maze was busy. Try the move again!' in response.text:
            while 'Last Move: FAILED because the maze was busy. Try the move again!' in response.text:
                response = session.get(url + value)
        time.sleep(0.5)

    print(response.text)
