<h3> Logan2 HackMyVM </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6ee416e6-9dff-4e7d-b716-f675dda98ad4)

After downloading the attached vm and importing it in virtual box while spawning it I had to discover the host

So here's what it looks like discovering the host on the subnet

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4af52131-f6cb-4387-b329-1ad1cf707536)
```r
sudo netdiscover
```

Cool now let's get to the hacking 

![hacking_cat](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c78f3689-62e0-4448-97ca-70e6a854e228)

First thing first is always `NMAP` scan
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a6250cdc-547e-4656-90fa-981828576189)

```r
nmap -sCV -A -p22,80,3000 -oN nmapscan 192.168.8.227
```

So we have a web server running on port 80 & 3000 while port 22 is ssh

I added the domain `logan.hmv` to my `/etc/hosts` file just to easily reference the machine rather than using the ip

Going over to port 80 shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dd6478a9-05de-4d72-9169-dc2294f21637)

Nothing interesting? From viewing page source I saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1a8a4c39-b4af-46d6-b8fa-a8b28cdb0ad5)

It's loading a javascript file

Viewing the file showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64ef6005-42d7-4a17-b176-d3c0c6837c63)

```js
document.addEventListener("DOMContentLoaded", function() {
    fetch('/save-user-agent.php', {
        method: 'POST',
        body: JSON.stringify({ user_agent: navigator.userAgent }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log('User-Agent saved successfully.');
        } else {
            console.error('Error saving User-Agent.');
        }
    })
    .catch(error => {
        console.error('Network error:', error);
    });
});
```

Looking at the file looks almost useless to me when I first saw it

But hmmm it actually sends the user agent value to the endpoint `/save-user-agent.php`

So I looked at my burp history for the request and got it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/174986a6-c903-43ea-9e17-f8e4508460ac)

I forwarded it to repeater to play with it


Here'
