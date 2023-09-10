<h3> Binary Search Algorithm </h3>

Binary Search is defined as a searching algorithm used in a sorted array by repeatedly dividing the search interval in half. The idea of binary search is to use the information that the array is sorted and reduce the time complexity to O(log N). 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fd62102c-2206-4b4c-ad3b-317bf6f99425)

Conditions for when to apply Binary Search in a Data Structure:

To apply Binary Search algorithm:
- The data structure must be sorted.
- Access to any element of the data structure takes constant time.

Binary Search Algorithm:

In this algorithm, 
- Divide the search space into two halves by finding the middle index "mid". 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/22ba339c-76c5-42b2-a88e-cd1f6e65009d)
- Compare the middle element of the search space with the key. 
- If the key is found at middle element, the process is terminated.
- If the key is not found at middle element, choose which half will be used as the next search space.
  - If the key is smaller than the middle element, then the left side is used for next search.
  - If the key is larger than the middle element, then the right side is used for next search.
- This process is continued until the key is found or the total search space is exhausted.

How to Implement Binary Search?

The Binary Search Algorithm can be implemented in the following two ways
- Iterative Binary Search Algorithm
- Recursive Binary Search Algorithm

Complexity Analysis of Binary Search:

Time Complexity: 
- Best Case: O(1)
- Average Case: O(log N)
- Worst Case: O(log N)

Auxiliary Space: O(1), If the recursive call stack is considered then the auxiliary space will be O(logN).

Advantages of Binary Search:
- Binary search is faster than linear search, especially for large arrays.
- More efficient than other searching algorithms with a similar time complexity, such as interpolation search or exponential search.
- Binary search is well-suited for searching large datasets that are stored in external memory, such as on a hard drive or in the cloud.

Drawbacks of Binary Search:
- The array should be sorted.
- Binary search requires that the data structure being searched be stored in contiguous memory locations. 
- Binary search requires that the elements of the array be comparable, meaning that they must be able to be ordered.

Applications of Binary Search:
- Binary search can be used as a building block for more complex algorithms used in machine learning, such as algorithms for training neural networks or finding the optimal hyperparameters for a model.
- It can be used for searching in computer graphics such as algorithms for ray tracing or texture mapping.
- It can be used for searching a database.

SOURCE: [GeeksForGeeks](https://www.geeksforgeeks.org/binary-search/)

#### Example 1:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9bbd3097-bbce-42fb-930f-55072f8ef15f)

Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

Let us look at the first example case they gave us:

```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```

So we are to find the index position of a target value in an array

The best algorithm to use here of cause is Binary Search because the list is sorted 

First thing we need is this:

```
L = 0
R = len(nums) - 1
mid = L + (R - L) // 2
target = 9
```

Now we will start from the center of the array:

```
[-1,0,3,5,9,12]
```

The center index of the array is 3

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fcaf2ea3-6b98-4b2c-ac31-1d454744b436)

```
>>> nums = [-1,0,3,5,9,12]
>>> L = 0
>>> R = len(nums) - 1
>>> mid = L + (R - L) // 2
>>> target = 9
>>> 
>>> nums[mid]
3
>>>
```

Now we check the condition:
- Is the array index of the middle number equal to the target value? If it is return the middle number!
- Is the array index of the middle number less than the target value? If it is shift the search space to the right by setting `L` to `mid + 1` and repeating the process!
- Is the array index of the middle number greater than the target value? If it is shift the search space to the left by setting `R` to `mid - 1` and repeating the process!

That's the logic of `Iterative Binary Search Algorithm` since we will be doing this in a loop and not recursively

Doing that manually wouldn't take time since this array is small in terms of the length

But it's best to put your coding skill in practice

So I wrote a script to solve that!

Here's the script:

```python
# Iterative Binary Search Algorithm

def binarySearch(arr, x):
    l = 0
    r = len(arr)-1

    while l <= r:
        
        mid = l + (r - l) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] < x:
            l = mid + 1

        else:
            r = mid - 1
        
    return -1


arr = [-1,0,3,5,9,12]
x = 9

result = binarySearch(arr, x)
print(result)
```

Using it I got the value of the target which is 4
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5f39e2cf-9663-4fc5-a1da-056411bb65c2)


We can run the script and use the other case sample
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/66192e51-2fd3-4812-9caf-ae66dba0112d)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/49dd9e6e-b346-446f-bbae-b101c31cefca)

It returned `-1` because the target value we are searching for isn't among the array

Here's a sample script using Recursive Binary Search

```python
# Recursive Binary Search Algorithm

def binarySearch(arr, x, l, r):
    mid = l + (r-l)//2

    while r >= 0:

        if arr[mid] == x:
            return mid
        
        elif arr[mid] < x:
            return binarySearch(arr, x, l+1, r)
        
        else:
            return binarySearch(arr, x, l, mid-1)


arr = [-1,0,3,5,9,12]
x = 9
l = 0
r = len(arr)-1

result = binarySearch(arr, x, l, r)
print(result)
```

Now that we have a working solution we can now use the submission template and write the code there
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a80459c-b491-4db8-93e9-1e72f97ec148)

Wait what `Time Limit Exceeded`!!

Is python this slow for their time complexity?

But it takes very less seconds when I run it on my laptop
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/791d13c8-b37a-4f28-a3f1-f429788ea3b8)

Well since it's their custom Class they maybe will add some time complexity which my program didn't succeed in passing it

Now what?

Well I moved to C++ since it's more faster 

Here's the code

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int n = nums.size();
        int r = n - 1;
        int l = 0;
        
        while (l <= r) {
            int m = l + (r - l) / 2; 
            
            if (nums[m] == target)
                return m;
            
            if (nums[m] < target)
                l = m + 1;
            
            else
                r = m - 1;
        }
        
        return -1; 
    }
};
```

Running it I passed the custom testcase with a program runtime of 0ms 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c814ee4e-26a2-471c-85e6-797172edab41)

Now I can submit the code and boom it worked!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/33e41211-36d7-4383-a9f8-27e11fbcea04)

I was wondering why python didn't work so I checked the script and found a bug :(
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/90ad4f96-90f6-4ab1-9758-8575e6eaf9bc)

The middle variable is supposed to be inside the while loop
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c3c1abd6-fbc5-4421-9cf1-1f355cb608b1)

So after making that edit it worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/534bb318-b4f8-48cb-b75e-ac4d2ac26bca)

But still C++ is pretty much faster 🙂

#### Example 2
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ccb974f-9391-4ff1-b640-228d72a8b6c5)

Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

Ok so the question is pretty understandable!

We are going to be given a non-negative integer `x` and we are to provide it's square root without using any builtins function like pow()

This seemed intimidating to me at first when I tried it but after few minutes of thinking I got a breakthrough

First let's take a case sample from the challenge

```
Input: x = 4
Output: 2
Explanation: The square root of 4 is 2, so we return 2.
```

Given the number `4` what's the square root?

Here's my approach:

Of cause we should know that the square root of a number is a factor of a number that, when multiplied by itself, gives the original number

With that we just need to find an integer whereby if we take the square of it i.e multiply it with itself we will get the number 4

We can do that with like brute force approach i.e

```
1 * 1 == 4 False
2 * 2 == 4 True
```

That works! But let's say the number is large?

Well then this method will take some significant amount of time 

And we should know that when we submit a working solution it will also check it based on time complexity i.e there's a time limit expected for a program to run

So it's best we make our program more optimized and time efficient

Now how do we achieve that?

This is what I thought 🤔

If we can create an array in the range of the target number we can then use binary search algorithm to get the number we are looking for

Let's take two logical examples of what I'll do:

```
Input: x = 16
Output: 4
Explanation: The square root of 16 is 4, so we return 4.
```

First we create an array in the range of the input value:

```
➜  Learn python3
Python 3.11.2 (main, Feb 12 2023, 00:48:52) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> num = 16
>>> array = [i for i in range(1, num)]
>>> 
>>> array
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
>>>
```

Notice that I started my range from `1 to num` and not `0 to num` 

Having 0 is not really an issue but for case where 0 will be the answer is when the input is 0

Now that we have the array and since it's sorted we can apply binary search algorithm here

Basically we'll check if the `array[middle] * array[middle] == target`

```
➜  Learn python3
Python 3.11.2 (main, Feb 12 2023, 00:48:52) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> num = 16
>>> array = [i for i in range(1, num)]
>>> 
>>> array
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
>>> 
>>> left = 0
>>> right = len(array)-1
>>> middle = left + (right - left) // 2
>>> 
>>> square = array[middle]*array[middle]
>>> 
>>> square
64
>>> 
>>> square == num
False
>>> 
```

Well we can see that the comparison returned False and that's true because the statement is False

Next we can shift the search space to the left since the value compared with is greater than the input value

```
>>> right = middle - 1
>>> middle = left + (right - left) // 2
>>> square = array[middle]*array[middle]
>>>                                                                                                                                                                                          
>>> square
16                                                                                                                                                                                           
>>>                                                                                                                                                                                          
>>> square == num                                                                                                                                                                            
True                                                                                                                                                                                         
>>>
```

Now that returns True because 16 is indeed equal to 16

So the square root of the number 16 will be the `array[middle]` and that's 4

```
>>> array[middle]                                                                                                                                                                            
4                                                                                                                                                                                            
>>>
```

With that we've optimized the search

How about case two?

```
Input: x = 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.
```

With just looking at the input number we can tell that it isn't a perfect square

Perfect squares are numbers whose square roots are whole numbers

In this case we are asked to return the approximated value of the nearest integer

So if we are suppose to have a float number i.e 4.123105625617661 the approximate value will be 4

With that said let's get to it

First I'll get the array of numbers within the input range

```
>>> num = 8
>>> array = [i for i in range(1, num)]
>>> 
>>> array
[1, 2, 3, 4, 5, 6, 7]
>>>
```

Then I'll store the required parameters and start the logic

```
>>> left = 0
>>> right = len(array) - 1
>>> middle = left + (right - left) // 2
>>> 
>>> square = array[middle]*array[middle]
>>> 
>>> square == num
False
>>> 
>>> square
16
>>>
```

So we see that the square is greater than input value 

We can shift our search space to the right

```
>>> right = middle - 1
>>> middle = left + (right - left) // 2
>>> square = array[middle]*array[middle]
>>> 
>>> square
4
>>> 
>>> square == num
False
>>>
```

Ok now the comparison returned False and that's True since the value of square is 4 and the input number is 8

In this case this condition of the program comes in:

```python
if square < num:
  left = middle + 1
```

So there isn't really any more range again for this because if we move the search space to the right then the condition which shifts the search space to the left triggers 

Therefore since no more range for this the answer returned would be `array[middle]` which is `2`

```
>>> array[middle]
2
>>>
```

With that said we now understand how to implement this algorithm in solving this task

Here's my solve script

```python
def sqrt(num):
    array = [i for i in range(1, num)]
    left = 0
    right = len(array) - 1
    ans = -1
    
    if num == 0:
        return -1

    while left <= right:
        middle = left + (right - left) // 2
        square = array[middle] * array[middle]

        if square == num:
            ans = array[middle]
            break

        elif square > num:
            right = middle - 1

        else:
            left = middle + 1
            ans = array[middle]  

    return ans

num = 16
result = sqrt(num)
print(result)
```

Brief explanation of the conditional checks happening there:
- If square is equal to `num`, it means we have found the square root, and I update `ans` with the current value because it is indeed the square root.
- If square is less than `num`, we need to move the search range to the right, so you update `left` to `middle + 1`. However, we do not update `ans` in this case because the current value of `array[middle]` is not the square root; it's smaller.
- If square is greater than `num`, we need to move the search range to the left, so I update `right` to `middle - 1`. In this case, we do not update `ans` either because, again, the current value of `array[middle]` is not the square root; it's larger.


We can check for it's authenticity by running it with various testcases
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f7d8d451-10fd-41b3-9eb2-ccae7553015f)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b2ef420-bc55-484c-912f-1cf9faca15c3)

Now imagine using large number?
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a0711e53-09db-478a-85d6-0db880c2f538)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/792a8dc8-a436-4cec-812f-73057abf328d)

The time it took was just `0.14s` if you compare this with the brute force approach you will notice significant difference in time

Now that we're done let's paste it in the template given to this

I submitted it and got a wrong answer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/262e9bf8-5d19-4a05-8f71-1cf5dbfd746c)

I then remember I didn't check constraint 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1390a404-46c3-4b13-96a9-d761da1964a3)

So the input number can be within range 0 

Editing my script to use the right range, removing the if check comparing the number with 0 & changin the `ans` variable from `-1` to `0`

```python
def sqrt(num):
    array = [i for i in range(num+1)]
    left = 0
    right = len(array) - 1
    ans = 0

    while left <= right:
        middle = left + (right - left) // 2
        square = array[middle] * array[middle]

        if square == num:
            ans = array[middle]
            break

        elif square > num:
            right = middle - 1

        else:
            left = middle + 1
            ans = array[middle]  

    return ans

num = int(input())
result = sqrt(num)
print(result)
```

Then on running it again I got this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7414a9f9-39c2-4146-adaa-5c08566ffeef)

The program actually uses a lot of memory due the fact I'm saving the range in a loop and if a very large number is given it would take lot of memory maybe even crashing your laptop if you dont have high ram :(

So I decided to figure a way to optimize the code

After research I figured that the use of creating that array is not memory efficient as we can directly work on the number even without it being in an array (cool right?)

Modification to the script lead me to this:

```python
def sqrt(num):
    left, right = 0, num
    ans = 0

    while left <= right:
        middle = left + (right - left) // 2
        square = middle * middle

        if square == num:
            ans = middle
            break

        elif square > num:
            right = middle - 1

        else:
            left = middle + 1
            ans = middle  

    return ans

num = int(input())
result = sqrt(num)
print(result)
```

I used it on the template and it worked ^^
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7a2d7eef-e756-4d85-95ab-1017ddd55636)

Compared to when I used the array methd :( and this which directly works on the number, using a large number didn't crash my laptop but instead gave me it's square root in `0.09s`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/05104508-6b4e-4669-942e-5175ec44ac18)

#### Example 3
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/25d91b44-409c-43a3-998f-621d572d3428)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/27685c98-0273-4ea8-af33-f3d4dcae277d)

We are playing the Guess Game. The game is as follows:

I pick a number from 1 to n. You have to guess which number I picked.

Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.

You call a pre-defined API int guess(int num), which returns three possible results:

    -1: Your guess is higher than the number I picked (i.e. num > pick).
    1: Your guess is lower than the number I picked (i.e. num < pick).
    0: your guess is equal to the number I picked (i.e. num == pick).

Return the number that I picked.

So basically we are going to be given `n` whose range is between `1 <= n <= 231 - 1`

Our goal is to call the `guess` function which is already predefined in the code

The function requires an argument to be passed into it which is the number to be guessed

The goal of this task is to guess the right number

We can easily just brute force it depending on the value of `n` since the number to be guessed is in the range of `n` i.e `1 <= pick <= n`

But I won't do that because of it will take time and our code needs to be as fast as possible

Looking at the description they also gave us a good return result value needed to solve this

```
-1: Your guess is higher than the number I picked (i.e. num > pick).
1: Your guess is lower than the number I picked (i.e. num < pick).
0: your guess is equal to the number I picked (i.e. num == pick).
```

From that we can basically determine if our number is greater than the picked number or less or equal

This gives us a good chance to use Binary Search Algorithm

Just the standard logic 

Here's my solve script which is in it's template form

```python
class Solution(object):
    def guessNumber(self, n):
        """
        :type n: int
        :rtype: int
        """
        lower, higher = 1, n
        
        while lower <= higher:
            middle = lower + (higher - lower) // 2
            result = guess(middle)
            
            if result == 0:
                return middle
        
            elif result == -1:
                higher = middle - 1
            
            else:
                lower = middle + 1
```

Submitting it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/60db0e09-e52d-41b2-9df0-fa0fe1e9d0ae)


#### Example4

Description: Alice has some cards with numbers written on them. She arranges the cards in decreasing order, and lays them out face down in a sequence on a table. She challenges Bob to pick out the card containing a given number by turning over as few cards as possible. Can you help Bob locate the card:

```
cards = [8, 8, 6, 6, 6, 6, 6, 6, 3, 2, 2, 2, 0, 0, 0]
query = 6
```

The key note is that the card list is arranged in decreasing sequence which makes Binary Search Algorithm a gateway to solve this

Well since the query of the expected card is `6` that's an issue

Cause looking at the numbers in the card we can see there are quite retition of `6`s

And if we apply Binary Search it will return the middle number which in this case is `6`

So that's a false result because there are other 6's before it making it not the first occurrence

To solve this I'll basically do this:
- Make a function to get right index value that does this:
  - Check if `cards[mid]` is equal to query if it is then I do this:  
    - Check if `mid-1` is greater than or equal to `0` this is to avoid going out of bound of the `cards` array and then checking if `cards[mid-1] == query` this is to check if there are other poccurrence        of the query value aside the current one we have in the left hand side
    - If that check return True then we return `left` else we return "found"
    - Else we check if the `cards[mid]` is less than query if it is then we return "left"
    - Else we return "right" because that is when `cards[mid]` is greater than query
   
Then using the normal standard Binary Search Algorithm I'll get the right value

Here's my solve script

```python
def getRightIndex(cards, query, mid):
    mid_number = cards[mid]

    if mid_number == query:
        if mid-1 >= 0 and cards[mid-1] == query:
            return "left"
        else:
            return "found"

    elif mid_number < query:
        return "left"

    else:
        return "right"

def binarySeach(cards, query):
    left, right = 0, len(cards) -1 

    while left <= right:
        mid = left + (right - left) // 2
        r = getRightIndex(cards, query, mid)

        if r == "found":
            return mid

        elif r == "left":
            right = mid + 1
        
        else:
            left = mid - 1
    
    return -1


cards = [8, 8, 6, 6, 6, 6, 6, 6, 3, 2, 2, 2, 0, 0, 0]
query = 6

r = binarySeach(cards, query)
print(r)
```

Running it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8049d8d2-2f56-477c-ad1f-f1d63f3c9575)

We can confirm it is indeed right because it's the first occurrence of `6` in it's respective index value
