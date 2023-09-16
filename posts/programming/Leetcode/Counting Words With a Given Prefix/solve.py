def prefixCount(words, pref):
    count = 0
    n = len(pref)

    for i in words:
        if i[:n] == pref:
            count += 1

    return count

words = ["lewsmb","lewrydnve","lewqqm","lewec","lewn","lewb","lewedb"]
pref = "lew"
r = prefixCount(words, pref)

print(r)
