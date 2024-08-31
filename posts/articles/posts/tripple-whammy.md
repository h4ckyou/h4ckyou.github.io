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

















