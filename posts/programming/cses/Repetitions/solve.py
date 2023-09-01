def findLongestRepetition(sequence):
    maxRepetition = 0 
    currentRepetition = 1
    previousChar = sequence[0]

    for char in sequence[1:]:
        if char == previousChar:
            currentRepetition += 1
        else:
            maxRepetition = max(maxRepetition, currentRepetition)
            currentRepetition = 1
            previousChar = char

    return max(maxRepetition, currentRepetition)

sequence = list(input())
r = findLongestRepetition(sequence)

print(r)
