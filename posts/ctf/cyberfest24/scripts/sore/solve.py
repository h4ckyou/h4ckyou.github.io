import string
import subprocess

flag = ""
charset = string.ascii_letters + '_{}'

while True:
    for char in charset:
        command = f"echo {flag+char} | ./patched"
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, err = execute.communicate()
        print(f"Trying {flag+char}")

        if 'Wrong' not in output:
            flag += char
            break
    
    if flag[-1] == "}":
        break

print(f"FLAG: {flag}")
