def removeAnagrams(words):
    try:
        for i in range(1, len(words)):
            for j in range(1, len(words)):
                current = "".join(sorted(words[i]))
                previous = "".join(sorted(words[i-1]))
                
                if current == previous:
                    words.pop(i)
                
    except IndexError:
        pass
            
    return words

words = ["a", "b", "a"]
r = removeAnagrams(words)

print(r)
