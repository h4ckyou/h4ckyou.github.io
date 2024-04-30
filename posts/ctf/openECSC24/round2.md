<h3> openECSC CTF 2024 ( Round 2) </h3>

Good day, here I'll be giving the writeup to the few challenges I was able to solve during the ctf

#### Another round, another sanity check 

Just the standard "sanity check" challenge, going over to their discord challenge in the "announcement" group gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6e921c7e-dc1d-4131-be44-67cadb5c7039)

```
Flag: openECSC{ldepywBS5XUBYHLeVDo6+mK7iFHFhwhwY0+LjR3R9EI=}
```

#### Blind Maze
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/301e0bb1-be91-4aea-9389-25c1b35f9e49)

We are given a pcap file and after downloading the attachment I opened it up in Wireshark
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/abd6bec2-ef13-4806-80db-8bc77ed87dfe)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7bcd9120-3011-4c8d-95f5-2a8bb9884d64)

The first noticable thing is that this contains http requests

And on looking at the protocol hierachy shows it contains mostly http request
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dc5a46d0-f4b0-40f0-a007-5b6191616752)

Following the tcp stream I saw that it's basically solving a web based maze challenge where direction `start` initializes the game and gives us a session cookie and `up, down, left & right` are the paths used to move around the maze
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a228b6ce-93b3-4b12-9faa-6625dc7da907)

At the last http request that is after solving the maze finish the flag is shown to us
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e004a9b9-95ad-4a70-8a1d-f0fb0fcad315)

Apparently this didn't involve us solving it at our end and it turned out to be an unintended solution so they released a `revenge` sequel of the challenge

```
Flag: openECSC{i_found_a_map_e1871a60}
```

#### Revenge of the Blind maze
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c6157194-7b31-4a53-b349-6df447630ee8)

It's very identical to the previous one but this time around the flag isn't in the pcap file meaning we would need to solve it

During the process of trying to solve it I spent quite some time on it because i didn't bother to understand how the maze worked

Here's what I did:
- I extracted all the paths from the pcap using python
- Sent the extracted path to the provided instance

This didn't work then I started debugging

From looking through various packets I concluded that when a user sends a path to the server there's a possibility of it being not processed which then the user needs to resend the path

Here's how that failed chance looks here
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e5f03a03-8910-441f-95ef-faaa233940af)

So if we get that we then need to resend the path as shown here
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1b10a0a6-6c9c-4f2f-be5d-2c8675450673)

With that said my initial path which I extracted contained repetitive paths i.e the path which are valid and the ones which are repeated again due to failure

In order to extract just the valid path I checked for the case where by the path given fails

With that said it's then simple to solve 

Another thing is that we can get the "failed" message multiple times but that can be easily fixed by just resending the path till it works

Here's the script I used to extract the paths from the pcap file: [extract](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/openECSC24/scripts/round2/Blind%20Maze%20Revenge/extract.py)

```python
import re

def extract_paths(content):
    pattern = r'Last Move: (.+?)</h4>'
    paths = re.findall(pattern, content)
    return paths

def filter_successful_paths(paths):
    return [path for path in paths if "FAILED" not in path]

file = ["response1.txt", "response2.txt", "response3.txt"] 
exp = []

for f in file:
    with open(f, "r") as file:
        content = file.read()
        path = extract_paths(content)
        filtered = filter_successful_paths(path)

        exp += filtered

exp.append('right') # --> it kinda missed this part which was the last value of the maze path

with open("direction.txt", "w") as f:
    for line in exp:
        f.write(line + '\n')
```

And finally the [solve](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/openECSC24/scripts/round2/Blind%20Maze%20Revenge/solve.py) script

```python
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
```

Running the script works and we get the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b9ada3d5-4432-40b3-a584-59389f5ecc74)

```
Flag: openECSC{flag_inside_the_attachment_yes_we_like_it_bb01b0d5}
```




