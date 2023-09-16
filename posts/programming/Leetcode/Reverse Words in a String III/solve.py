def reverseWords(s):
    arr = s.split()
    r = []

    for i in range(len(arr)):
        r.append(arr[i][::-1])

    return " ".join(r)

s = "Let's take LeetCode contest"
r = reverseWords(s)

print(r)
