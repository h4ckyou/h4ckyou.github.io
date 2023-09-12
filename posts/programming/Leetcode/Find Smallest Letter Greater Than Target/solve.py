def nextGreatestLetter(letters, target):
    for letter in letters:
        if letter > target:
            return letter
    
    return letters[0]


letters = ["x","x","y","y"]
target = "z"

r = nextGreatestLetter(letters, target)
print(r)
