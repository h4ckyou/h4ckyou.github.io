So this challenge was very identical to BabyFirstWeb Revenge from HITCON CTF

Running the script would create a webshell

But you need your public ip address so as to retrieve the path to where the webshell uploaded:

```
$sandbox = md5("Aguns" . "127.0.0.1");
```

From here you can run php command:

```
/c.php?cmd=system("cat /home/flag.txt")
```
