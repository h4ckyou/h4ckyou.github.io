<h3> Hackerrank: Runner-Up </h3>

Description: 

```
Given the participants' score sheet for your University Sports Day, you are required to find the runner-up score.
You are given scores.
Store them in a list and find the score of the runner-up. 
```

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8b4cf2e4-70b5-4efa-890d-001417eac252)

Input Format:

```
The first line contains n.
The second line contains an array of integers each separated by a space.
```

Constraints:

```
- 2 ⩽ n ⩽ 10
- -100 ⩽ A[i] ⩽ 100
```

So our goal is to find the second runner up in a given number of scores

There are various ways to solve this

But here's my own thought solution process

My solution involves:
- Getting the difference between the maximum value of the score with each of the numbers in the score 
- The lowest value returned will be the maximum value i.e max - A[i] > max - max
- Then in a list I'll put all the numbers which are not the maximum value
- I will then get the minimum value of that list and get its index of the difference array
- The corresponding index of the difference array will be the same as the score array

Here's my solve script

```python
def getRunnerUp(array, N):
    difference = [(N - j) for j in array]
    maxValue = min(difference)
    exclusiveMax = [i for i in difference if i != maxValue]
    minimum = min(exclusiveMax)
    idx = difference.index(minimum)

    return array[idx]

if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))

    result = getRunnerUp(arr, max(arr))
    print(result)
```

It works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6de7e24d-8638-46e7-9f12-1dabefa5e267)



