<h3> Repetition </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e35d337b-3921-4795-802e-08ed5ba402d2)

Description:

```
You are given a DNA sequence: a string consisting of characters A, C, G, and T.
Your task is to find the longest repetition in the sequence.
This is a maximum-length substring containing only one type of character.
```

So what this is about is:
- We will receive a DNA sequence which is a string consisting of characters
- The goal is to find the amount of times a character is being repeated the most

For example if they give:
- AAABBCCDDDD

The answer should be 4 because letter `D` is repeated 4 times

To solve this I'll do this:
- Make the received input as a list
- Define a function which does this:
  - I will iterate through the sequence of characters and keep track of the current repetition length and the character being repeated
  - When the sequence changes, I will compare the current repetition length with the longest repetition length encountered so far and update accordingly
 
Here's my solve script

```python
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
```

It works 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9d943d36-da83-4f32-bd4f-b16eaf401308)
