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

#### Anti-rev
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5bc16728-9f8d-48bf-b371-119bd2953543)

We are given an executable file and running it to get an overview of what it does shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/077a0960-67bd-4ef1-ad68-f10cff082fa6)

This seems like we would need to find the expected input inorder to get the right output

Throwing it into a decompiler which in my case IDA gave something like [this](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/openECSC24/scripts/round2/Anti-Rev/diss.c)

Note that's the decompilation from using dogbolt 

IDA didn't decompile it well and from looking at the control flow graph i saw it had just so many branches

And looking at the disassembly in gdb shows lots of `nops` & `add` instruction
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/11672227-5ecc-4265-9b9e-fc50b4ee1a57)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38d3a94e-0cbf-4171-9af9-6e503e888020)

I suppose this is preventing us from reversing it as the challenge name implies

In order to get around this I first thought of patching the `nops & add` with a `ret` but then I remember this can actually be quite the job for [angr](https://github.com/angr/angr)

So yeah I just grabbed a sample template from [here](https://book.hacktricks.xyz/reversing/reversing-tools-basic-methods/angr/angr-examples)

In our case the win condition is if we get "Correct!" and we would like to avoid any path that would lead to us getting "Wrong!"

Here's the solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/openECSC24/scripts/round2/Anti-Rev/solve.py)

Running it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/529c84e2-14eb-4cb8-b291-4b43306c2d8d)

```
Flag: openECSC{f4nCy_n0p5!_745fb2f2}
```

#### WOauth a laundry!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/77412b59-b06d-48db-9dd2-01f5a94bccd0)

We are given a web instance to connect to and on going there shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fb186d5a-957c-4f1f-851f-d1b1bc59e45d)

We can't view anything as we are not authenticated

Since there's a login button at the left edge i clicked on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d793323-2b1a-4dc5-8361-c6c7f52b173c)

It surprisingly worked without even asking for any form of authentication 🤔

We can view the availble laundries or amenities
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d94c88a8-1f8f-4b17-8240-e50aef7f3226)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b9d7ed32-9cb6-42a6-bd8e-11507d027130)

I didn't see anything of interest here

Checking the session storage shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/76aa5c27-58f5-4420-a187-48f6bf5adcc1)

The value of `admin` is set to `0` we probably want it to be `1` inorder to view other things?

As of now changing it from the client side won't really do much at the server side so let's take a look at the request handling the login

I logged out then relogin while intercepting the request

First it does a `GET` request to the `creds` api endpoint
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f441e5df-c063-4f07-bb89-a53458735ce6)

Intercepting the response to the request shows the `client_id & client_secret`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7156afc1-9d6e-492d-9b5a-3c8eb25fa517)

The next request shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dadb3865-300c-4f47-92a1-2013b0e79e60)

This is making a connection via `openid` which is an interoperable authentication protocol based on the OAuth 2.0 framework [src](https://openid.net/developers/how-connect-works/)

And looking at the parameters passed as the query I saw this

```
scope=openid laundry amenities
```

We can assume that this scope determines what we as an authenticated user would have access to

I appended `admin` to it since that happens to be a `key` value in the session storage
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/968d3698-d2dc-4742-a769-f51cce28bd56)

The request seems to work because it was able to generate the access token bearer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38269974-f0ce-4a3d-a3c7-9f9730a56334)

But after doing that I still noticed the `admin` value in the session is `0`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cc5b066c-e05b-4877-8060-bc36637b9291)

Weird.

So i decided to look for endpoint that might be useful

I viewed the page source and saw it's importing a js file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4133852b-fe2b-4a4b-9891-a3a4189d6b7b)

```
./_app/immutable/entry/app.Ck9duSk9.js
```

I accessed it from the browser but the result looks bad
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/08157786-5796-44bb-8358-fa8ecb22a2b0)

We can easily js beautifier it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/399e5c49-2aec-4d7f-8a1a-05026ba726b8)

Scrolling down the js file shows a new endpoint
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8815b8f3-ff0e-46f7-b452-a7974d214560)

```js
const ae = [() => v(() => import("../nodes/0.DwINNMcl.js"), __vite__mapDeps([0, 1, 2, 3, 4, 5, 6, 7, 8]), import.meta.url), () => v(() => import("../nodes/1.COoiP6uJ.js"), __vite__mapDeps([9, 1, 2, 10, 6]), import.meta.url), () => v(() => import("../nodes/2.CngkQmog.js"), __vite__mapDeps([11, 1, 2, 4, 12, 6, 7]), import.meta.url), () => v(() => import("../nodes/3.D75S8dhM.js"), __vite__mapDeps([13, 1, 2, 3, 4]), import.meta.url), () => v(() => import("../nodes/4.LaKRB8Xm.js"), __vite__mapDeps([14, 1, 2, 12, 4, 15, 5]), import.meta.url), () => v(() => import("../nodes/5.BpDOC5ki.js"), __vite__mapDeps([16, 1, 2, 12, 4, 15, 5]), import.meta.url)],
    le = [],
    fe = {
        "/": [2],
        "/admin": [3],
        "/amenities": [4],
        "/laundry": [5]
    },
    ce = {
        handleError: ({
            error: a
        }) => {
            console.error(a)
        },
        reroute: () => {}
    };
export {
    fe as dictionary, ce as hooks, re as matchers, ae as nodes, oe as root, le as server_loads
};
```

Let's try accessing `/admin`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ebc6f4d9-4e0d-4799-8980-18a0b449be54)

It shows a generate button

I confirmed if this is accessible from a normal user and it is but when clicking the button nothing happens
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/03d156af-4973-4f07-b32a-45353fed9e98)

On the other hand since we have admin as part of the scope it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/150eb85b-f239-4467-bb2c-702c16c044ff)

But from the content of what's generated we would like to maybe change it

Looking at the request that handles the pdf generation shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fc883fde-dbd1-48ac-956f-54668afc8e15)

Unfortunately the body isn't in the request and we would like to maybe edit it?

I started searching through various js files

And eventually I found a js file that handles the pdf generation

I can't find it again and i'm lazy to start searching through the whole js files (yes i did this manually 💀)

The body expected was:

```js
{
    "requiredBy": "John Doe"
}
```

I tried this and it worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/22c74d21-2726-4ceb-968c-91d830726c95)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d7bac40b-8547-4416-9539-7c682faa85f9)

At this point we need to exfiltrate the flag 

I was familiar with a technique which can be used then all I needed was just to search it up

From searching it I found [this](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/server-side-xss-dynamic-pdf)

In my case I used the `iframe` tag

```
<iframe src=file:///flag.txt></iframe>
```

Using that works and I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dadc7ff1-1155-44c4-90c9-fbf765e302e8)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ce40d9ad-caac-4417-8667-b1d22d2df479)

```
Flag: openECSC{On3_l4uNdrY_70_ruL3_7h3m_4l1!_d208a530}
```

Thanks for reading!



























