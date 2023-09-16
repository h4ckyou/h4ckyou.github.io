<h3> Maximum Number of Words Found in Sentences </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4f08c124-4089-4e56-8ef6-145ac02226ad)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/95884ad5-9445-453d-b1bf-fd45f1c5e7d2)

A sentence is a list of words that are separated by a single space with no leading or trailing spaces.

You are given an array of strings `sentences`, where each `sentences[i]` represents a single sentence.

Return the maximum number of words that appear in a single sentence.

#### Approach 

My approach involves using list comprehension to get the sum of the words in the first sentence from `sentences[0]` 

Then I iterate through `1, len(sentences)` and compare the sum of `sentence[i]` with the initial maximum number 

If it's greater then i set the maximum number to the current sum

After going through all the sentence from the array I return the value of maximum

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Leetcode/Maximum%20Number%20of%20Words%20Found%20in%20Sentences/solve.py)
![omo](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/089fe177-2180-4fff-a512-c53120ce45c8)

The complexity is kinda horrible :(

