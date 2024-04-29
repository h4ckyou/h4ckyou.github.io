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
