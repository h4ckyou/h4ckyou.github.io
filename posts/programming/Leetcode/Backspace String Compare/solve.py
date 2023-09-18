def backspaceCompare(s, t):
    s = list(s)
    t = list(t)
    s_reformed = []
    t_reformed = []

    for i in range(len(s)):
        s_reformed.append(s[i])
        if s_reformed[-1] == "#":
            if len(s_reformed) == 1:
                s_reformed.pop()
            else:
                s_reformed.pop(len(s_reformed)-1)
                s_reformed.pop(len(s_reformed)-1)
    
   
    for j in range(len(t)):
        t_reformed.append(t[j])
        if t_reformed[-1] == "#":
            if len(t_reformed) == 1:
                t_reformed.pop()
            else:
                t_reformed.pop(len(t_reformed)-1)
                t_reformed.pop(len(t_reformed)-1)
    
    # print(s_reformed)
    # print(t_reformed)

    if s_reformed == t_reformed:
        return True
    else:
        return False

s = "a#c"
t = "b"
r = backspaceCompare(s, t)

print(r)
