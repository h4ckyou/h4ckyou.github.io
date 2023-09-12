def substring2(array, s1):
    hashtable = {}

    for i in range(len(array)):
        for j in range(i+1, len(array)):
            if j - i == 2:
                array[i], array[j] = array[j], array[i]
                
                if ("".join(array)) in hashtable:
                    hashtable[("".join(array))] += 1
                else: 
                    hashtable[("".join(array))] = 1

                array = list(s1)

    return list(hashtable)


def substring1(array, s1):
    hashtable = {}

    for i in range(len(array)):
        for j in range(i+1, len(array)):
            if j - i == 2:
                array[i], array[j] = array[j], array[i]
                hashtable[("".join(array))] = 1                
                array = list(s1)
    
    r = list(hashtable)

    for i in list(hashtable):
        r += substring2(list(i), i)

    return r

def canBeEqual(s1, s2):
    array = list(s1)
    substring = substring1(array, s1)

    if s2 in substring:
        return True
    else:
        return False
                
s1 = "bnxw"
s2 = "bwxn"

r = canBeEqual(s1, s2)
print(r)
