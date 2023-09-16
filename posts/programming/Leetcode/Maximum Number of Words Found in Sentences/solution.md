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

The complexity is kinda horrible :( so let's optimize it xD

The idea is simple first we notice that each sentence are separated with space `" "`

So we can count the number of spaces in `sentences` and append to a list

Basically instead of counting the number of words we just count the number of spaces

And python has a function that can help us do it that's why I'm going with this approach

Now that we would have a list contaning the number of spaces we will get it's max value and add `1` to it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d57e69f8-e8ac-48a6-8970-c1eaceda44a3)

Adding `1` to the max result gives you the number of words in the sentence, which is one more than the maximum number of spaces. 

Submitting it shows it's way more faster
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/db47cd48-c45d-4ec6-89f9-738fe50a15d8)

```python
class Solution:
    def mostWordsFound(self, sentences: List[str]) -> int:
        #### Overkill ####
        # maximum = sum(1 for i in sentences[0].split())

        # for i in range(1, len(sentences)):
        #     if sum(1 for j in sentences[i].split()) > maximum:
        #         maximum = sum(1 for j in sentences[i].split())
        
        # return maximum

        c = []
        for i in sentences:
            c.append(i.count(" "))
        return max(c)+1
```
