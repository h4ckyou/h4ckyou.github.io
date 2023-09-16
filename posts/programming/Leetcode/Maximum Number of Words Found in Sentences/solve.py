def mostWordsFound(sentences):
    maximum = sum(1 for i in sentences[0].split())

    for i in range(1, len(sentences)):
        if sum(1 for j in sentences[i].split()) > maximum:
            maximum = sum(1 for j in sentences[i].split())
    
    return maximum
    
sentences = ["alice and bob love leetcode", "i think so too", "this is great thanks very much"]
r = mostWordsFound(sentences)

print(r)
