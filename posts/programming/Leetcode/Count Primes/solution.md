<h3> Count Primes </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/69121a52-bb69-468b-bfbc-8f6aff7b71c9)

Given an integer `n`, return the number of prime numbers that are strictly less than `n`.

The question is very straight forward and it's clear on what we're to do

First my approach was I needed to find a way to get all the numbers within `n-1` range

And then iterating over the list and comparing if it's less than `n` which I'll increase the counter is the statement if True

But I had problem with generating the list of prime numbers **I suck at math which is bad :(**  so I looked at the hint and it gave the algorithm to use

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/37c9b22a-6cf1-42a7-86d6-3c37213cc526)

Cool upon checking google on that I got [this](https://www.geeksforgeeks.org/sieve-of-eratosthenes/)

With that algorithm **Sieve of Eratosthenes** we can get the list of prime numbers within a specific `n` range

Then from that the remaining part is easy as we can just iterate through the prime numbers list and check for the condition 

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Count%20Primes/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/78e8e12f-1f39-4e83-925a-fb73f6b7ba7f)
