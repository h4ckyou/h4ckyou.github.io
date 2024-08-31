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
























