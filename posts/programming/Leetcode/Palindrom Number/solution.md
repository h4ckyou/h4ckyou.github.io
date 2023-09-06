<h3> Palindrome Number</h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c1586e37-71f6-4837-af1c-d16fd3277610)

Given an integer x, return true if x is a palindrome and false otherwise.

#### Solution

First what's a palindrome number? 

Well, An integer is a palindrome when it reads the same forward and backward.

For example, 121 is a palindrome while 123 is not.

Now we just need to return True is a number is palindrome and False if it isn't

The case here is simple because we can tell if it's a palindrome number when the 0th index and last index are the same

And as for all single digit number they will always return True because it reads the same forward and backward

To solve this I'll convert the integer to a string then perform the python slicing and the if condition

Well that's what I thought till I came around this test case input:

```
1000021
```

If I run it against the program I made it will return True 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/443daef8-201d-432b-aa0b-a8f4b5097215)

But that's wrong because it doesn't meet the condition of an integer being palindrome

So we need to make sure that it reads the same forward and backward

We need a way to compare each value starting from the middle element of the number spreading left and right 

For example:

Let's say the input is 12345

Then we need to get the middle element which in this case is 3

Now we need to start comparing:

```
input[i:middle] with input[middle:i]
```

That way we will check if:

```
2 == 4,
1 == 5
```

Or vice versa i.e starting compare from left to middle and right to middle

The logic is now this (I'll take the failed test case sample as an example):

```
x = 1000021

1 -> 0 -> 0 -> 0 -> 0 -> 2 -> 1
```

Now I'll get the left and right index which can be calculated as this:

```
left = 0
right = len(str(x)) - 1
```

In a while loop checking the condition while left is less than right

We will check:

```
is str(x)[left] == str(x)[right] ?
```

If it isn't true we will return False

Else we'll move the index towards the middle this is achieved by doing:

```
left = left + 1
right = right - 1
```

With that said here's my final script

```python
def isPalindrome(number):
    input = str(number)
    left, right = 0, len(input) - 1

    while left <= right:
        if input[left] != input[right]:
            return False

        left += 1
        right -= 1    

    return True

x = int(input())
r = isPalindrome(x)

print(r)
```

Submitting it worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0f551db4-066e-4f93-a86e-24ed1f17e551)




